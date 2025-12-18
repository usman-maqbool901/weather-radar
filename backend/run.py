#!/usr/bin/env python3
import uvicorn
from app.main import app
from app.utils.config import config

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=config.SERVER_PORT,
        log_level="info"
    )

