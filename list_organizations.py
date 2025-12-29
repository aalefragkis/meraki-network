import requests
import json
import sys

# 1. Load configuration from ignore_config.json
try:
    with open('ignore_config.json', 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print("Error: ignore_config.json file not found!")
    sys.exit()

# 2. Assign configuration values to variables
API_KEY = config['api_key']
BASE_URL = 'https://api.meraki.com/api/v1'

headers = {
    'X-Cisco-Meraki-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

print("Connecting to Meraki API...")
endpoint = f"{BASE_URL}/organizations"

try:
    response = requests.get(endpoint, headers=headers)
    
    # Check if the API call was successful (Status Code 200)
    if response.status_code == 200:
        organizations = response.json()
        print("\n--- Organization List ---")
        for org in organizations:
            print(f"Name: {org['name']}")
            print(f"ID: {org['id']}")
            print("-" * 25)
            
        # Summary for the user
        print(f"\nTotal organizations found: {len(organizations)}.")
    else:
        print(f"API Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"An error occurred during execution: {e}")