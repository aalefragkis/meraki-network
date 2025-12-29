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
ORG_ID = config['org_id']
ORG_NAME = config['org_name']

# Construct the API URL dynamically
BASE_URL = f'https://api.meraki.com/api/v1/organizations/{ORG_ID}/networks'

headers = {
    'X-Cisco-Meraki-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

print(f"Connecting to Organization: {ORG_NAME} (ID: {ORG_ID})")
print(f"Fetching networks...")

try:
    response = requests.get(BASE_URL, headers=headers)
    
    if response.status_code == 200:
        networks = response.json()
        print(f"\nFound {len(networks)} networks:")
        for net in networks:
            # Display network details: Name, Product Types, and ID
            print(f"- Network: {net['name']} | Types: {net['productTypes']} | ID: {net['id']}")
    else:
        print(f"API Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"An error occurred during execution: {e}")