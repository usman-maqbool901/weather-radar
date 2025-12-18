from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import radar
from app.utils.config import config
import asyncio

app = FastAPI(title="Weather Radar API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(radar.router, prefix="/api/radar", tags=["radar"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    from app.services.scheduler import start_scheduler
    asyncio.create_task(start_scheduler())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.SERVER_PORT)
