import requests
import json
import sys

# 1. Load configuration settings
try:
    with open('ignore_config.json', 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print("Error: ignore_config.json file not found!")
    sys.exit()

# 2. Assign configuration variables
API_KEY = config['api_key']
NET_ID = config['network_id']
LOCATION = config['location']

# API Endpoint for devices within a specific network
url = f'https://api.meraki.com/api/v1/networks/{NET_ID}/devices'

headers = {
    'X-Cisco-Meraki-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

print(f"Fetching device list for location: {LOCATION}...")

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        devices = response.json()
        print(f"\n--- Network Devices at {LOCATION} ({len(devices)}) ---")
        
        for dev in devices:
            # Extract device details with fallbacks for missing names
            name = dev.get('name', 'Unnamed Device')
            model = dev.get('model', 'Unknown Model')
            mac = dev.get('mac', 'N/A')
            print(f"Device: {name} | Model: {model} | MAC: {mac}")
            
    else:
        print(f"API Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"An error occurred during data retrieval: {e}")