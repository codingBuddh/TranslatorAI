from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TranslatorAI"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LANGSMITH_ENDPOINT: str = os.getenv("LANGSMITH_ENDPOINT", "")
    LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY", "")
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "")

    class Config:
        case_sensitive = True

settings = Settings() 