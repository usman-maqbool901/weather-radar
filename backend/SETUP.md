# FastAPI Backend Setup

## Quick Start

1. **Install dependencies:**
```bash
cd backend_python
pip install -r requirements.txt
```

2. **Run the server:**
```bash
python3 run.py
```

The server will start on `http://localhost:8000`

## Testing

Test the API:
```bash
# Health check
curl http://localhost:8000/health

# Get radar data (wait ~1 minute for first fetch)
curl http://localhost:8000/api/radar/latest
```

Or use the test script:
```bash
python3 test_api.py
```

## Project Structure

```
backend_python/
├── app/
│   ├── main.py              # FastAPI application
│   ├── routes/
│   │   └── radar.py         # API routes
│   ├── services/
│   │   ├── mrms_fetcher.py  # Fetch MRMS data
│   │   ├── grib2_parser.py  # Parse GRIB2 files
│   │   ├── data_cache.py    # In-memory cache
│   │   └── scheduler.py     # Background scheduler
│   └── utils/
│       └── config.py        # Configuration
├── test_grib2_simple.py     # GRIB2 parser script
├── run.py                   # Server startup
└── requirements.txt         # Dependencies
```

## API Endpoints

- `GET /health` - Health check
- `GET /api/radar/latest` - Get latest radar data (GeoJSON)

## Notes

- The scheduler automatically fetches new data every 5 minutes
- First data fetch happens on server startup (may take ~30-60 seconds)
- Data is cached in memory for fast responses

