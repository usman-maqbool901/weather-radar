# Weather Radar Backend (FastAPI)

Python FastAPI backend for the Weather Radar application.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python3 run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

## API Endpoints

- `GET /health` - Health check
- `GET /api/radar/latest` - Get latest radar data

## Environment Variables

- `PORT` - Server port (default: 5000)

