import os

class Config:
    MRMS_BASE_URL = "https://mrms.ncep.noaa.gov/data"
    MRMS_RALA_PATH = "/2D/ReflectivityAtLowestAltitude/"
    UPDATE_INTERVAL = 5 * 60
    CACHE_TTL = 10 * 60
    SERVER_PORT = int(os.getenv("PORT", 8000))
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ]

config = Config()

