# Docker Setup - Simple Two-Service Architecture

This setup runs the frontend and backend as separate services for easy deployment and demonstration.

## Quick Start

1. **Create a `.env` file** in the project root:
   ```bash
   VITE_MAPBOX_TOKEN=your_mapbox_token_here
   ```

2. **Start both services**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Health Check: http://localhost:8000/health

## Services

### Backend (Port 8000)
- FastAPI server
- Serves radar data API
- Health check endpoint at `/health`

### Frontend (Port 3000)
- React + Vite development server
- Connects to backend at `http://localhost:8000`
- Hot module replacement enabled

## Docker Compose Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up --build

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f frontend
docker-compose logs -f backend

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Environment Variables

Set in `.env` file or pass directly:

- `VITE_MAPBOX_TOKEN` (required): Your Mapbox access token
- `VITE_API_URL` (optional): Backend API URL (default: `http://localhost:8000`)
- `PORT` (optional): Backend port (default: `8000`)
- `MRMS_BASE_URL` (optional): MRMS data source URL

## Architecture

```
┌─────────────┐         ┌─────────────┐
│  Frontend   │────────▶│   Backend   │
│  Port 3000  │  HTTP   │  Port 8000  │
│  (Vite)     │         │  (FastAPI)  │
└─────────────┘         └─────────────┘
```

- Frontend runs Vite dev server with HMR
- Backend runs FastAPI with uvicorn
- Frontend makes API calls to `http://localhost:8000`
- CORS is configured to allow all origins

## For Client Demo

This setup is perfect for demonstrations:

1. **Simple**: Two services, easy to understand
2. **Accessible**: Both services exposed on standard ports
3. **Live Updates**: Frontend has hot reload for quick changes
4. **Health Checks**: Backend includes health check endpoint

## Troubleshooting

### Port already in use
Change ports in `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # Frontend
  - "8001:8000"  # Backend
```

### Frontend can't connect to backend
- Ensure backend is running: `docker-compose ps`
- Check backend logs: `docker-compose logs backend`
- Verify backend health: `curl http://localhost:8000/health`

### Mapbox token issues
- Verify token in `.env` file
- Check frontend logs: `docker-compose logs frontend`
- Ensure token starts with `pk.` (public token)