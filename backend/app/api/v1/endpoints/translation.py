from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from app.services.langchain_service import TranslationService

router = APIRouter()
translation_service = TranslationService()

class TranslationRequest(BaseModel):
    text: str
    source_language: Optional[str] = None
    target_languages: List[str]

class TranslationResponse(BaseModel):
    translations: dict[str, str]

@router.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    try:
        translations = await translation_service.batch_translate(
            text=request.text,
            target_languages=request.target_languages
        )
        return TranslationResponse(translations=translations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 