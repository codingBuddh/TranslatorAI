from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field
from app.services.langchain_service import TranslationService

router = APIRouter()
translation_service = TranslationService()

class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to translate")
    source_language: Optional[str] = Field(None, description="Source language code (optional)")
    target_languages: List[str] = Field(..., min_items=1, description="List of target language codes")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Hello world",
                "source_language": None,
                "target_languages": ["es", "fr"]
            }
        }

class TranslationResponse(BaseModel):
    translations: dict[str, dict[str, str]]

@router.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        if not request.target_languages:
            raise HTTPException(status_code=400, detail="At least one target language is required")

        translations = await translation_service.batch_translate(
            text=request.text,
            target_languages=request.target_languages
        )
        
        return TranslationResponse(translations=translations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 