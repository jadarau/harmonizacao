from __future__ import annotations
from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def file_status():
    return {"status": "ok", "message": "File API is running"}