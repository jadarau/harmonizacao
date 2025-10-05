from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes.chat import router as chat_router
from app.api.routes.file import router as file_router

app = FastAPI(title="Chat API (Groq + FastAPI)", version="1.0.0")

if settings.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(chat_router)
app.include_router(file_router, prefix="/file", tags="file")