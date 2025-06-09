from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class GazetteEntryProcess(BaseModel):
    """
    Schema for processing a gazette entry.
    """
    processed_text: Optional[str] = Field(
        None, 
        description="The processed/parsed text from the gazette entry"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, 
        description="Additional metadata extracted from the entry"
    )
    has_errors: bool = Field(
        False, 
        description="Whether there were errors during processing"
    )
    error_message: Optional[str] = Field(
        None, 
        description="Error message if processing failed"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "processed_text": "Processed text content...",
                "metadata": {
                    "company_name": "Example Corp",
                    "tax_number": "1234567890",
                    "extracted_fields": {
                        "address": "123 Example St, City",
                        "capital": "1.000.000 TL"
                    }
                },
                "has_errors": False,
                "error_message": None
            }
        }
    }
