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
        # Set environment to suppress ECCODES warnings
        env = os.environ.copy()
        env['ECCODES_WARNINGS'] = '0'
        
        # Run the parser script
        result = subprocess.run(
            ["python3", str(script_path), temp_file_path],
            capture_output=True,
            text=True,
            timeout=120,
            env=env,
            cwd=str(base_path)  # Run in backend directory where script expects output
        )
        
        # Output file is created in the script's working directory (backend/)
        output_file = base_path / "test_output.geojson"
        
        # Filter out ECCODES warnings from stderr (these are non-fatal)
        stderr_lines = result.stderr.split('\n') if result.stderr else []
        filtered_stderr = [
            line for line in stderr_lines 
            if not line.strip().startswith('ECCODES ERROR') 
            and not 'Truncating time' in line
            and not 'non-zero seconds' in line
            and line.strip()  # Keep non-empty lines
        ]
        filtered_stderr_text = '\n'.join(filtered_stderr)
        
        # Check if output file was created (this indicates success)
        if output_file.exists():
            # Success! Warnings in stderr are OK if file was created
            if filtered_stderr_text.strip():
                print(f"Parser completed with warnings (non-fatal): {filtered_stderr_text[:200]}")
        else:
            # Output file doesn't exist - check if script failed
            if result.returncode != 0:
                # Script failed - show the actual error
                error_msg = filtered_stderr_text or result.stdout
                if error_msg.strip():
                    raise RuntimeError(f"Python parser failed: {error_msg}")
                else:
                    raise RuntimeError("Python parser failed with no error message")
            else:
                # Script returned 0 but no output file - this shouldn't happen
                raise FileNotFoundError(
                    f"Python parser completed but did not generate output file at {output_file}. "
                    f"Stdout: {result.stdout[-500:] if result.stdout else 'empty'}"
                )
        
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

