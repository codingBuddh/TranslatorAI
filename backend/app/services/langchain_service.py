import logging
import os
from typing import Dict
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langsmith import Client
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Configure environment variables for LangSmith
os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY
os.environ["LANGSMITH_ENDPOINT"] = settings.LANGSMITH_ENDPOINT
os.environ["LANGSMITH_PROJECT"] = settings.LANGSMITH_PROJECT
os.environ["LANGCHAIN_TRACING_V2"] = "true"

class TranslationService:
    def __init__(self):
        try:
            logger.info("Initializing TranslationService...")
            
            # Initialize LangSmith client
            self.langsmith_client = Client()
            logger.info("LangSmith client initialized")
            
            self.llm = ChatOpenAI(
                model="gpt-4",
                temperature=0.1,
                api_key=settings.OPENAI_API_KEY
            )
            
            # Translation prompt template
            self.translation_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert translator.
                 If there are HTML markups, remove them. Give the outputs in a very simple format.
                 If there is any math, keep the numbers and symbols unchanged.
                 
                 Translate the following text to {target_language}.
                 Maintain the original meaning, tone, and style while ensuring natural and fluent output."""),
                ("user", "{text}")
            ])

            # Create the translation chain
            self.translation_chain = LLMChain(
                llm=self.llm,
                prompt=self.translation_prompt,
                verbose=True
            )
            logger.info("Translation service initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing TranslationService: {str(e)}")
            raise

    async def translate(self, text: str, target_language: str) -> str:
        """Translate text to target language"""
        try:
            logger.info(f"Translating to {target_language}")
            response = await self.translation_chain.ainvoke(
                {
                    "text": text,
                    "target_language": target_language
                },
                config={
                    "tags": [settings.LANGSMITH_PROJECT],
                    "metadata": {
                        "operation": "translation",
                        "target_language": target_language
                    }
                }
            )
            return response["text"].strip()
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            raise

    async def detect_language(self, text: str) -> str:
        """Detect the language of the input text"""
        try:
            detect_prompt = ChatPromptTemplate.from_messages([
                ("system", "Detect the language of the following text and respond with only the language name:"),
                ("user", "{text}")
            ])
            
            detect_chain = LLMChain(llm=self.llm, prompt=detect_prompt)
            response = await detect_chain.ainvoke(
                {"text": text},
                config={
                    "tags": [settings.LANGSMITH_PROJECT],
                    "metadata": {"operation": "language_detection"}
                }
            )
            return response["text"].strip()
        except Exception as e:
            logger.error(f"Error detecting language: {str(e)}")
            raise

    async def batch_translate(self, text: str, target_languages: list[str]) -> Dict[str, Dict[str, str]]:
        """Translate text to multiple target languages"""
        translations = {}
        try:
            source_language = await self.detect_language(text)
            logger.info(f"Batch translation from {source_language} to {target_languages}")
            
            for language in target_languages:
                try:
                    translation = await self.translate(text, language)
                    translations[language] = {
                        "text": translation,
                        "source_language": source_language
                    }
                    logger.info(f"Successfully translated to {language}")
                except Exception as e:
                    logger.error(f"Error translating to {language}: {str(e)}")
                    translations[language] = {
                        "error": str(e),
                        "source_language": source_language
                    }
            
            return translations
        except Exception as e:
            logger.error(f"Batch translation failed: {str(e)}")
            raise 