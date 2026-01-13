#!/usr/bin/env python3
import uvicorn
from app.main import app
from app.utils.config import config

import os

from dotenv import load_dotenv
# Load .env file from parent directory (project root)
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

if __name__ == "__main__":
    # Note: Token injection is no longer needed since frontend runs as separate service
    # Frontend gets VITE_MAPBOX_TOKEN from environment variables
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=config.SERVER_PORT,
        log_level="info"
    )

