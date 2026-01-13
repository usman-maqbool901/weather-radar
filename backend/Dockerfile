FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including eccodes and GRIB2 libraries
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gfortran \
    curl \
    libeccodes-dev \
    libgfortran5 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY . .

# Set environment variable to suppress ECCODES warnings
ENV ECCODES_WARNINGS=0

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "run.py"]
