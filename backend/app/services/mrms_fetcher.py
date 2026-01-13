import requests
import gzip
import time
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
    """
    Fetch the latest RALA GRIB2 file from MRMS.
    Retries up to 3 times if download fails or is incomplete.
    """
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            file_url = get_latest_file_url()
            print(f"Downloading from: {file_url} (attempt {attempt + 1}/{max_retries})")
            
            # Don't use Accept-Encoding: gzip - the file is already gzipped
            # Using it might cause the server to double-compress or send incomplete data
            response = requests.get(
                file_url,
                timeout=120,  # Increased timeout for large files
                headers={"User-Agent": "Mozilla/5.0 (compatible; WeatherRadar/1.0)"},
                stream=True  # Stream download to handle large files better
            )
            response.raise_for_status()
            
            # Check content length if available
            content_length = response.headers.get('Content-Length')
            if content_length:
                print(f"Expected file size: {int(content_length) / 1024 / 1024:.2f} MB")
            
            # Download content
            content = b''
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    content += chunk
            
            print(f"Downloaded {len(content) / 1024 / 1024:.2f} MB")
            
            # Verify we got some data
            if len(content) < 1000:  # GRIB2 files should be at least a few KB
                raise ValueError(f"Downloaded file too small: {len(content)} bytes")
            
            # Try to decompress
            try:
                compressed_data = BytesIO(content)
                with gzip.open(compressed_data, 'rb') as f:
                    decompressed_data = f.read()
                
                print(f"Decompressed to {len(decompressed_data) / 1024 / 1024:.2f} MB")
                
                if len(decompressed_data) < 1000:
                    raise ValueError(f"Decompressed file too small: {len(decompressed_data)} bytes")
                
                return decompressed_data, datetime.now()
                
            except gzip.BadGzipFile as e:
                # File might not be gzipped, try using it directly
                print(f"Warning: File might not be gzipped, using as-is: {e}")
                return content, datetime.now()
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Decompression error (attempt {attempt + 1}): {e}, retrying...")
                    time.sleep(retry_delay)
                    continue
                raise
            
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"Download error (attempt {attempt + 1}): {e}, retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                continue
            print(f"Error fetching RALA file after {max_retries} attempts: {e}")
            raise
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Error (attempt {attempt + 1}): {e}, retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                continue
            print(f"Error fetching RALA file after {max_retries} attempts: {e}")
            raise
    
    raise RuntimeError(f"Failed to fetch RALA file after {max_retries} attempts")

