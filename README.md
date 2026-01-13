# Weather Radar Application

A full-stack weather radar application that dynamically fetches and displays real-time radar data from MRMS (Multi-Radar Multi-Sensor) system.

## Features

- Real-time radar data from MRMS Reflectivity at Lowest Altitude (RALA)
- Interactive Mapbox visualization with heatmap rendering
- Dynamic data updates (refreshes show new data)
- Professional UI with modern design
- TypeScript for type safety
- Responsive design

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- cfgrib/xarray (GRIB2 parsing)
- requests (HTTP client)

### Frontend
- React 19 with TypeScript
- Vite
- Mapbox GL JS
- Tailwind CSS
- shadcn/ui components

## Prerequisites

- Node.js 22+ installed
- npm package manager
- Mapbox access token ([Get one here](https://account.mapbox.com/))

## Setup Instructions

### Backend Setup

1. Navigate to the backend_python directory:
```bash
cd backend_python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the server:
```bash
python3 run.py
```

Or with auto-reload for development:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will run on `http://localhost:8000` by default (port 8000 is often used by macOS system processes).

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the frontend directory:
```bash
cp .env.example .env
```

4. Add your Mapbox token to `.env`:
```
VITE_MAPBOX_TOKEN=your_mapbox_token_here
VITE_API_URL=http://localhost:8000
```

5. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000` by default.

## MRMS Data Handling

### Data Source
The application fetches data directly from MRMS (Multi-Radar Multi-Sensor) system at `https://mrms.ncep.noaa.gov/data/`. Specifically, it uses the **Reflectivity at Lowest Altitude (RALA)** product.

### Data Processing Flow

1. **Fetching**: The backend periodically (every 5 minutes) checks MRMS for the latest RALA GRIB2 file
2. **Parsing**: GRIB2 files are parsed using `cfgrib/xarray` library (Python-based, more reliable for MRMS data)
3. **Transformation**: Parsed data is converted to GeoJSON FeatureCollection format
4. **Caching**: Processed data is cached in memory to avoid re-parsing on every request
5. **Serving**: Frontend fetches cached data via REST API endpoint `/api/radar/latest`

### Update Frequency
- Backend checks for new data every 5 minutes
- Cache TTL is set to 10 minutes
- Frontend can manually refresh or auto-refresh (optional)

### Data Decimation
For performance optimization, the application decimates data points if the dataset is too large (>50,000 points), sampling every Nth point to maintain smooth rendering.

## Library Justifications

### cfgrib/xarray
**Why**: Python-based GRIB2 parsing library that handles more GRIB2 templates than Node.js alternatives. More reliable for MRMS data which uses product definition template 55072 (not supported by grib2-simple).

### Mapbox GL JS
**Why**: Industry-standard library for interactive map rendering. Implementing custom map rendering would be impractical and time-consuming.

### shadcn/ui
**Why**: Provides accessible, well-designed UI components. Building a complete component library from scratch would exceed time constraints while maintaining quality.

### Vite
**Why**: Fast development experience with HMR and optimized production builds. Significantly faster than alternatives like Create React App.

## Trade-offs and Assumptions

### Assumptions
1. **MRMS File Discovery**: Assumes latest file can be determined via directory listing HTML parsing
2. **GRIB2 Format**: Uses cfgrib/xarray which supports MRMS product definition template 55072
3. **Coordinate System**: Assumes data uses standard lat/lon coordinates (normalized from 0-360° to -180-180°)
4. **Update Cadence**: MRMS updates approximately every 2-5 minutes

### Trade-offs
1. **Data Decimation**: Large datasets are sampled to maintain performance, potentially losing some detail
2. **In-Memory Caching**: Cache is lost on server restart (acceptable for this use case)
3. **Error Handling**: Graceful degradation when data is unavailable
4. **No Authentication**: API endpoints are open (acceptable for demo/assessment)
5. **Python Backend**: Switched from Node.js to Python for better GRIB2 parsing support

### Known Limitations
- GRIB2 parsing may have limitations with very complex MRMS structures
- Large datasets may require further optimization
- No persistent storage of historical data

## Future Improvements

- Add data persistence (database for historical data)
- Implement WebSocket for real-time updates
- Add user preferences (auto-refresh interval, color schemes)
- Implement data export functionality
- Add multiple radar product support
- Improve error recovery and retry logic

## Project Structure

```
/backend_python
  /app
    /routes       # API routes
    /services     # Business logic (MRMS fetcher, parser, cache, scheduler)
    /utils        # Configuration
  main.py         # FastAPI app entry point
  run.py          # Server startup script

/frontend
  /src
    /components   # React components
    /hooks        # Custom React hooks
    /lib          # Utilities (API client, Mapbox init)
    /types        # TypeScript type definitions
    /utils        # Constants and formatters
  App.tsx        # Main app component
```

## License

ISC

