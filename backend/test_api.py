#!/usr/bin/env python3
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health():
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_radar_latest():
    print("\nTesting /api/radar/latest endpoint...")
    print("Waiting for data to be fetched (this may take a minute)...")
    
    max_attempts = 12
    for i in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/api/radar/latest", timeout=10)
            if response.status_code == 200:
                data = response.json()
                features_count = len(data.get("data", {}).get("features", []))
                print(f"✅ Success! Got {features_count} features")
                print(f"Last updated: {data.get('lastUpdated')}")
                return True
            elif response.status_code == 503:
                print(f"Attempt {i+1}/{max_attempts}: Data not ready yet, waiting...")
                time.sleep(5)
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"Attempt {i+1}/{max_attempts}: Server not responding, waiting...")
            time.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    print("❌ Timeout waiting for data")
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("FastAPI Backend Test")
    print("=" * 60)
    
    if test_health():
        test_radar_latest()
    else:
        print("❌ Health check failed - server may not be running")
        print("Start server with: python3 run.py")

