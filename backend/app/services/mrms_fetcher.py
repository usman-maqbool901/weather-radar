import requests
import gzip
from io import BytesIO
from datetime import datetime
from app.utils.config import config
import re

def get_latest_file_url() -> str:
    base_url = f"{config.MRMS_BASE_URL}{config.MRMS_RALA_PATH}"
    
    try:
        response = requests.get(
            base_url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0 (compatible; WeatherRadar/1.0)"}
        )
        response.raise_for_status()
        
        html = response.text
        
        latest_file_pattern = r'href="([^"]*MRMS_ReflectivityAtLowestAltitude\.latest\.grib2\.gz)"'
        latest_match = re.search(latest_file_pattern, html, re.IGNORECASE)
        
        if latest_match:
            latest_file = latest_match.group(1)
            print(f"Found .latest file: {latest_file}")
            if latest_file.startswith("http"):
                return latest_file
            elif latest_file.startswith("/"):
                return f"{config.MRMS_BASE_URL}{latest_file}"
            else:
                return f"{base_url}{latest_file}"
        
        patterns = [
            r'href="([^"]+\.grib2\.gz)"',
            r"href='([^']+\.grib2\.gz)'",
        ]
        
        files = set()
        for pattern in patterns:
            matches = re.finditer(pattern, html, re.IGNORECASE)
            for match in matches:
                filename = match.group(1).strip()
                if filename.endswith(".grib2.gz") and "Parent" not in filename:
                    files.add(filename)
        
        if not files:
            print(f"HTML response sample: {html[:1000]}")
            raise ValueError("No GRIB2 files found in directory listing")
        
        file_array = sorted(files, reverse=True)
        latest_file = file_array[0]
        
        if latest_file.startswith("http"):
            file_url = latest_file
        elif latest_file.startswith("/"):
            file_url = f"{config.MRMS_BASE_URL}{latest_file}"
        else:
            file_url = f"{base_url}{latest_file}"
        
        print(f"Found {len(files)} GRIB2 files, using: {latest_file}")
        return file_url
        
    except Exception as e:
        print(f"Error fetching MRMS file list: {e}")
        raise

def fetch_latest_rala_file() -> tuple[bytes, datetime]:
    try:
        file_url = get_latest_file_url()
        response = requests.get(
            file_url,
            timeout=60,
            headers={"Accept-Encoding": "gzip"}
        )
        response.raise_for_status()
        
        compressed_data = BytesIO(response.content)
        with gzip.open(compressed_data, 'rb') as f:
            decompressed_data = f.read()
        
        return decompressed_data, datetime.now()
    except Exception as e:
        print(f"Error fetching RALA file: {e}")
        raise

