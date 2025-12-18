import asyncio
from datetime import datetime
from app.services.mrms_fetcher import fetch_latest_rala_file
from app.services.grib2_parser import parse_grib2_to_geojson
from app.services.data_cache import cache
from app.utils.config import config

_scheduler_task = None

async def update_radar_data():
    try:
        print("Fetching latest radar data...")
        buffer, timestamp = fetch_latest_rala_file()
        geo_json = parse_grib2_to_geojson(buffer)
        cache.set(geo_json, timestamp)
        print(f"Radar data updated at {datetime.now().isoformat()}")
    except Exception as error:
        print(f"Failed to update radar data: {error}")

async def scheduler_loop():
    await update_radar_data()
    
    while True:
        await asyncio.sleep(config.UPDATE_INTERVAL)
        await update_radar_data()

async def start_scheduler():
    global _scheduler_task
    if _scheduler_task is None or (_scheduler_task and _scheduler_task.done()):
        _scheduler_task = asyncio.create_task(scheduler_loop())
        print(f"Scheduler started with {config.UPDATE_INTERVAL}s interval")

def stop_scheduler():
    global _scheduler_task
    if _scheduler_task and not _scheduler_task.done():
        _scheduler_task.cancel()
        _scheduler_task = None

