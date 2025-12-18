#!/usr/bin/env python3
import uvicorn
from app.main import app
from app.utils.config import config

import os

from dotenv import load_dotenv
# Load .env file from parent directory (project root)
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

ACTUAL_TOKEN = os.getenv('VITE_MAPBOX_TOKEN', '')
if ACTUAL_TOKEN:
    print(f"Mapbox token loaded: {ACTUAL_TOKEN[:10]}...")
else:
    print("Warning: VITE_MAPBOX_TOKEN not found in environment variables")

# Function to replace content in files
def replace_in_file(file_path, placeholder, token):
    """Replace placeholder string with actual token in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()

        # Check if placeholder exists in file
        if placeholder not in file_contents:
            return False

        # Replace all occurrences of placeholder with the actual token
        file_contents = file_contents.replace(placeholder, token)

        # Write the updated contents back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(file_contents)
        print(f"Updated: {file_path}")
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def inject_mapbox_token():
    """Inject Mapbox token into built frontend JS files."""
    if not ACTUAL_TOKEN:
        print("Skipping token injection: No token available")
        return
    
    # Path to frontend dist/assets directory (relative to backend directory)
    frontend_dist_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist', 'assets')
    
    # Check if directory exists
    if not os.path.exists(frontend_dist_path):
        print(f"Frontend dist/assets directory not found: {frontend_dist_path}")
        print("Skipping token injection. Build the frontend first.")
        return
    
    # Common placeholder patterns to look for
    placeholders = [
        "VITE_MAPBOX_TOKEN_replaced"
    ]
    
    updated_count = 0
    # Walk through the directory and all subdirectories, but only update .js files
    for root, dirs, files in os.walk(frontend_dist_path):
        # Skip node_modules if it exists
        dirs[:] = [d for d in dirs if d != 'node_modules']
        
        for file_name in files:
            if file_name.endswith('.js'):
                file_path = os.path.join(root, file_name)
                for placeholder in placeholders:
                    if replace_in_file(file_path, placeholder, ACTUAL_TOKEN):
                        updated_count += 1
                        break  # Only replace once per file
    
    if updated_count > 0:
        print(f"Successfully updated {updated_count} file(s) with Mapbox token")
    else:
        print("No files were updated. Token may already be injected or placeholders not found.")

if __name__ == "__main__":
    # Inject Mapbox token into built frontend files before starting server
    inject_mapbox_token()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=config.SERVER_PORT,
        log_level="info"
    )

