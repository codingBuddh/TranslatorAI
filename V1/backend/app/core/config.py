from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TranslatorAI"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY", "")
    LANGSMITH_ENDPOINT: str = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "translator-ai")
    
    class Config:
        case_sensitive = True

    def __init__(self):
        super().__init__()
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        if not self.LANGSMITH_API_KEY:
            logger.warning("LANGSMITH_API_KEY not set. LangSmith tracing will be disabled.")

settings = Settings() 