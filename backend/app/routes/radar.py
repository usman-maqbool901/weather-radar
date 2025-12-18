from fastapi import APIRouter, HTTPException
from app.services.data_cache import cache

router = APIRouter()

@router.get("/latest")
async def get_latest_radar():
    cached = cache.get()
    
    if not cached:
        return {
            "error": "Radar data not available",
            "message": "Data is still being fetched. Please try again in a moment."
        }
    
    return cached

