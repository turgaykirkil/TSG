import logging
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from app.services import nlp_service

logger = logging.getLogger(__name__)

router = APIRouter()

class NlpRequest(BaseModel):
    text: str

@router.post("/parse-announcement", response_model=Dict[str, Any])
async def parse_text(
    request_body: NlpRequest
):
    """
    Receives raw text and uses the NLP service to parse it,
    extracting structured information like company name, address, etc.
    """
    logger.info("Received request for NLP parsing.")
    if not request_body.text or not request_body.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")

    try:
        # Ensure the model is loaded before parsing
        if nlp_service.nlp_model is None:
            nlp_service.load_spacy_model()
            
        parsed_data = nlp_service.parse_announcement_text(request_body.text)
        logger.info("Successfully parsed text.")
        return parsed_data
    except Exception as e:
        logger.error(f"An error occurred during NLP parsing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to parse text due to an internal server error: {e}")
