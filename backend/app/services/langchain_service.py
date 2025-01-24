import os
import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
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
            
            # Initialize LLM
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.1,
                streaming=True
            )
            logger.info("LLM initialized successfully")
            
            # Initialize LangSmith client
            self.langsmith_client = Client()
            logger.info("LangSmith client initialized")
            
            # Initialize memory
            self.memory = ConversationBufferMemory(
                return_messages=True,
                memory_key="chat_history"
            )
            logger.info("Memory initialized")

            # Enhanced translation prompt template
            self.translation_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert translator with deep knowledge of multiple languages and cultures.
                Follow these rules for translation:
                1. Maintain the original meaning, tone, and style
                2. Ensure natural and fluent output in the target language
                3. Preserve any technical terms or proper nouns
                4. Keep formatting and punctuation appropriate for the target language
                5. If there are culturally specific terms, provide appropriate translations or explanations
                
                Target Language: {target_language}"""),
                ("user", "{text}")
            ])

            # Create the translation chain
            self.translation_chain = LLMChain(
                llm=self.llm,
                prompt=self.translation_prompt,
                memory=self.memory,
                verbose=True
            )
            logger.info("Translation chain created successfully")
            
        except Exception as e:
            logger.error(f"Error initializing TranslationService: {str(e)}")
            raise

    async def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text
        """
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

    async def translate(self, text: str, target_language: str) -> str:
        """
        Translate text to target language using LangChain
        """
        try:
            # Detect source language
            source_language = await self.detect_language(text)
            logger.info(f"Detected source language: {source_language}")
            
            # Add source language info to memory
            self.memory.chat_memory.add_message(
                SystemMessage(content=f"Source language detected: {source_language}")
            )
            
            # Execute the translation chain
            response = await self.translation_chain.ainvoke(
                {
                    "text": text,
                    "target_language": target_language
                },
                config={
                    "tags": [settings.LANGSMITH_PROJECT],
                    "metadata": {
                        "operation": "translation",
                        "source_language": source_language,
                        "target_language": target_language
                    }
                }
            )
            
            return response["text"].strip()
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            raise

    async def batch_translate(self, text: str, target_languages: list[str]) -> Dict[str, Any]:
        """
        Translate text to multiple target languages
        """
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