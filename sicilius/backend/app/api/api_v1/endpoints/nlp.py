import logging
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

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

@router.post("/parse-announcements", response_model=List[Dict[str, Any]])
async def parse_text_multiple(
    request_body: NlpRequest
):
    """
    Splits the incoming OCR text into multiple announcements and parses each segment.
    Returns a list where each item contains the structured fields plus
    `index`, `sicil_office_header`, and `original_text`.
    """
    logger.info("Received request for MULTI NLP parsing.")
    if not request_body.text or not request_body.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")

    try:
        if nlp_service.nlp_model is None:
            nlp_service.load_spacy_model()

        parsed_list = nlp_service.parse_multiple_announcements(request_body.text)
        logger.info("Successfully parsed multiple announcements. count=%d", len(parsed_list))
        return parsed_list
    except Exception as e:
        logger.error(f"An error occurred during MULTI NLP parsing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to parse text due to an internal server error: {e}")
