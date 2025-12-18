import json
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, Any

def parse_grib2_to_geojson(buffer: bytes) -> Dict[str, Any]:
    base_path = Path(__file__).parent.parent.parent
    script_path = base_path / "test_grib2_simple.py"
    
    if not script_path.exists():
        raise FileNotFoundError(f"Python parser script not found: {script_path}")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".grib2") as temp_file:
        temp_file.write(buffer)
        temp_file_path = temp_file.name
    
    try:
        result = subprocess.run(
            ["python3", str(script_path), temp_file_path],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout
            raise RuntimeError(f"Python parser failed: {error_msg}")
        
        output_file = Path.cwd() / "test_output.geojson"
        if not output_file.exists():
            raise FileNotFoundError("Python parser did not generate output file")
        
        with open(output_file, 'r') as f:
            geojson = json.load(f)
        
        if not geojson.get("features"):
            raise ValueError("No features extracted from GRIB2 file")
        
        print(f"Extracted {len(geojson['features'])} data points from GRIB2 file")
        return geojson
        
    finally:
        try:
            os.unlink(temp_file_path)
        except:
            pass

