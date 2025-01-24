from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import translation
from app.core.config import settings

app = FastAPI(title="TranslatorAI API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    translation.router,
    prefix=settings.API_V1_STR,
    tags=["translation"]
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to TranslatorAI API",
        "docs": "/docs",
        "version": "1.0.0"
    } 