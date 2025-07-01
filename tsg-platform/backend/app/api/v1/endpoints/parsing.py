import io
from typing import List, Dict, Any, Optional
import pdfplumber
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel, Field

# --- Pydantic Models for Response Structure ---

class ParsedTable(BaseModel):
    """Defines the structure for a single parsed table from the PDF."""
    table_name: str = Field(..., description="A unique name for the table, e.g., 'Page 1 - Table 1'")
    headers: List[str] = Field(..., description="The list of cleaned header columns for this table.")
    rows: List[Dict[str, Any]] = Field(..., description="A list of rows, where each row is a dictionary mapping headers to cell values.")

# --- Router Definition ---

router = APIRouter()

# --- Helper Functions ---

def clean_cell(cell_content: Any) -> Optional[str]:
    """Cleans individual cell content by converting to string, stripping whitespace."""
    if cell_content is None:
        return None
    # Convert to string, strip whitespace, and return None if empty after stripping
    cleaned = str(cell_content).strip()
    return cleaned if cleaned else None

def find_table_header(table: List[List[Any]]) -> Optional[tuple[List[str], int]]:
    """
    Finds the first row in a table that contains actual content.
    This simple heuristic assumes the first non-empty row is the header.
    """
    for i, row in enumerate(table):
        cleaned_row = [clean_cell(cell) for cell in row]
        # If any cell in the cleaned row has content, we consider it a valid row.
        if any(cell is not None for cell in cleaned_row):
            # Use the cleaned row as the header, replacing any remaining Nones.
            final_header = [h if h is not None else f"column_{j+1}" for j, h in enumerate(cleaned_row)]
            return final_header, i
    return None

# --- API Endpoint ---

@router.post("/parse-pdf", response_model=List[ParsedTable])
async def parse_pdf_table(file: UploadFile = File(...)):
    """
    Parses a multi-page PDF into a single table using a simple and reliable strategy.
    1. Finds the header on the first page only.
    2. Uses that header as the single source of truth.
    3. Collects every non-header, non-empty row from all pages.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    try:
        file_content = await file.read()
        master_header: Optional[List[str]] = None
        all_data_rows: List[Dict[str, Any]] = []

        print("--- PDF PARSING V5 (FINAL): SIMPLE & RELIABLE STRATEGY ---")
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            # --- PASS 1: Find Master Header on First Page ONLY ---
            if not pdf.pages:
                raise HTTPException(status_code=404, detail="PDF is empty and has no pages.")

            print(f"--- PASS 1: Found {len(pdf.pages)} pages. Searching for header on first page... ---")
            first_page_tables = pdf.pages[0].extract_tables()
            if not first_page_tables:
                raise HTTPException(status_code=404, detail="No tables found on the first page.")

            for table_data in first_page_tables:
                header_info = find_table_header(table_data)
                if header_info:
                    master_header, _ = header_info
                    print(f"Master Header found: {master_header}")
                    break
            
            if not master_header:
                raise HTTPException(status_code=404, detail="Could not find any valid header on the first page.")

            # --- PASS 2: Collect ALL data rows from ALL pages ---
            print("--- PASS 2: Collecting all data rows from all pages... ---")
            for page_num, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                if not tables:
                    continue

                for table_data in tables:
                    for row_data in table_data:
                        cleaned_row = [clean_cell(cell) for cell in row_data]

                        # KURAL 1: Satır tamamen boşsa atla.
                        if not any(cell is not None for cell in cleaned_row):
                            continue

                        # KURAL 2: Satır, ana başlığın aynısıysa atla.
                        if cleaned_row == master_header:
                            print(f"Skipping header-like row on page {page_num + 1}")
                            continue

                        # Bu bir veri satırıdır, listeye ekle.
                        # Satırın uzunluğunu başlıkla eşleşecek şekilde ayarla.
                        while len(row_data) < len(master_header):
                            row_data.append(None)
                        if len(row_data) > len(master_header):
                            row_data = row_data[:len(master_header)]
                        
                        row_dict = dict(zip(master_header, row_data))
                        all_data_rows.append(row_dict)

        print(f"--- PARSING FINISHED: Found {len(all_data_rows)} total data rows. ---")

        # --- DIAGNOSTIC LOGGING ---
        print("\n--- DIAGNOSTIC START ---")
        print(f"[BACKEND-CHECK] Final Headers Sent to Frontend: {master_header}")
        print("[BACKEND-CHECK] First 5 Data Rows Sent to Frontend:")
        for i, row in enumerate(all_data_rows[:5]):
            print(f"  Row {i+1}: {row}")
        print("--- DIAGNOSTIC END ---\n")
        # --- END DIAGNOSTIC LOGGING ---

        if not all_data_rows:
            raise HTTPException(status_code=404, detail="No data rows could be extracted from the PDF.")

        final_merged_table = ParsedTable(
            table_name="Merged PDF Data",
            headers=master_header,
            rows=all_data_rows
        )

        return [final_merged_table]

    except Exception as e:
        import traceback
        print(f"Error parsing PDF: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An error occurred while parsing the PDF file: {str(e)}")
