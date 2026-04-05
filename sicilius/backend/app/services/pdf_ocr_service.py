import time
import logging
import httpx
from typing import Optional, Dict, Any, Tuple

try:
    from docling_core.types.doc.document import DoclingDocument
except ImportError:
    DoclingDocument = None
    logging.warning("'docling_core' Python library not found. Cannot convert JSON to Markdown.")

logger = logging.getLogger(__name__)

DOCLING_SERVE_URL = "http://localhost:5002/v1/convert/file"

async def extract_markdown_from_docling(
    file_bytes: bytes, 
    filename: str = "document.pdf"
) -> Tuple[Optional[str], Optional[Dict[str, Any]], Optional[int], float]:
    """
    Sends PDF bytes to the Docling AI backend.
    Returns: (markdown, json_payload, total_pages, processing_time)
    """
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=1200.0) as client:
            # Add parameters for better layout and column detection
            params = {
                "force_ocr": "true",
                "ocr_lang": "tur",
                "do_layout": "true"
            }
            # We use a tuple for the file upload explicitly to support the multipart form structure Docling expects
            files = [("files", (filename, file_bytes, "application/pdf"))]
            response = await client.post(DOCLING_SERVE_URL, files=files, params=params)
            
        processing_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            # The API might return a list if multiple files were uploaded, though we only upload one
            if isinstance(data, list) and len(data) > 0:
                data = data[0]
                
            if "status" in data and data["status"] == "success" and "document" in data:
                json_content = data["document"].get("json_content", {})
                
                # Convert backend JSON representation into standard Markdown
                markdown_content = ""
                if DoclingDocument:
                    try:
                        doc = DoclingDocument.model_validate(json_content)
                        markdown_content = doc.export_to_markdown()
                    except Exception as e:
                        logger.error(f"Docling model_validate export error: {e}")
                        markdown_content = f"<!-- Export Error: {e} -->"
                else:
                    markdown_content = "<!-- Docling core missing, raw JSON only -->"
                
                # Approximate the page count by inspecting the provenance of the final text layer
                pages = 1
                try:
                    if "texts" in json_content and len(json_content["texts"]) > 0:
                        prov = json_content["texts"][-1].get("prov", [])
                        if prov and len(prov) > 0:
                            pages = prov[0].get("page_no", 1)
                except Exception:
                    pass
                
                return markdown_content, json_content, pages, processing_time
            else:
                logger.error(f"Docling Invalid Response Struct: {data}")
        else:
            logger.error(f"Docling HTTP {response.status_code} Error: {response.text}")
            
    except Exception as e:
        logger.error(f"Failed connecting to AI Docling service: {e}")
        processing_time = time.time() - start_time
        
    return None, None, None, processing_time
