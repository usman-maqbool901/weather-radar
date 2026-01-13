#!/usr/bin/env python3
"""
Simple GRIB2 parser test using cfgrib/xarray (easier to install)
"""

import sys
import json
import gzip
import os
from pathlib import Path

# Suppress ECCODES warnings about timestamp truncation
os.environ['ECCODES_WARNINGS'] = '0'

try:
    import cfgrib
    import xarray as xr
except ImportError:
    print("Error: cfgrib and xarray are required")
    print("Install with: pip install cfgrib xarray")
    sys.exit(1)

def parse_grib2(file_path):
    """Parse GRIB2 file and convert to GeoJSON"""
    print(f"Opening GRIB2 file: {file_path}")
    
    try:
        ds = xr.open_dataset(file_path, engine='cfgrib')
        print(f"Dataset variables: {list(ds.data_vars)}")
        print(f"Dataset coordinates: {list(ds.coords)}")
        print(f"Dataset dimensions: {dict(ds.dims)}")
    except Exception as e:
        print(f"Error opening dataset: {e}")
        print("\nTrying to open with backend_kwargs...")
        try:
            ds = xr.open_dataset(
                file_path, 
                engine='cfgrib',
                backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround', 'level': 0}}
            )
        except Exception as e2:
            print(f"Error with backend_kwargs: {e2}")
            sys.exit(1)
    
    features = []
    decimation_factor = 20
    
    for var_name in ds.data_vars:
        var = ds[var_name]
        print(f"\nProcessing variable: {var_name}")
        print(f"  Shape: {var.shape}")
        print(f"  Coordinates: {list(var.coords)}")
        
        if 'latitude' in var.coords and 'longitude' in var.coords:
            lats = var.coords['latitude'].values
            lons = var.coords['longitude'].values
            values = var.values
            
            print(f"  Lat range: {lats.min():.2f} to {lats.max():.2f}")
            print(f"  Lon range: {lons.min():.2f} to {lons.max():.2f}")
            print(f"  Value range: {values.min():.2f} to {values.max():.2f}")
            
            if len(values.shape) == 2:
                rows, cols = values.shape
                
                count = 0
                for i in range(0, rows, decimation_factor):
                    for j in range(0, cols, decimation_factor):
                        if i < len(lats) and j < len(lons):
                            lat = float(lats[i])
                            lon = float(lons[j])
                            value = float(values[i, j])
                            
                            if value >= -10 and value <= 75:
                                lon_normalized = lon
                                if lon > 180:
                                    lon_normalized = lon - 360
                                
                                features.append({
                                    "type": "Feature",
                                    "geometry": {
                                        "type": "Point",
                                        "coordinates": [lon_normalized, lat]
                                    },
                                    "properties": {
                                        "reflectivity": round(value, 1)
                                    }
                                })
                                count += 1
                
                print(f"  Extracted {count} valid points")
    
    return features

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 test_grib2_simple.py <grib2_file_path>")
        print("\nExample:")
        print("  python3 test_grib2_simple.py file.grib2")
        print("  python3 test_grib2_simple.py file.grib2.gz")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not Path(file_path).exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    if file_path.endswith('.gz'):
        print("Decompressing gzip file...")
        decompressed_path = file_path.replace('.gz', '')
        with gzip.open(file_path, 'rb') as f_in:
            with open(decompressed_path, 'wb') as f_out:
                f_out.write(f_in.read())
        file_path = decompressed_path
        print(f"Decompressed to: {file_path}")
    
    try:
        features = parse_grib2(file_path)
    except Exception as e:
        print(f"\nError parsing GRIB2: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    if not features:
        print("\nWarning: No features extracted from GRIB2 file")
        sys.exit(1)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    output_file = "test_output.geojson"
    with open(output_file, 'w') as f:
        json.dump(geojson, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Success! Extracted {len(features)} data points")
    print(f"Output saved to: {output_file}")
    print(f"\nFirst 5 features:")
    for i, feature in enumerate(features[:5]):
        coords = feature['geometry']['coordinates']
        props = feature['properties']
        print(f"  {i+1}. Lat: {coords[1]:.4f}, Lon: {coords[0]:.4f}, "
              f"Reflectivity: {props['reflectivity']} dBZ")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

