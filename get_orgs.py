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

# 2. Assign API Key from configuration
API_KEY = config['api_key']
url = "https://api.meraki.com/api/v1/organizations"

headers = {
    "X-Cisco-Meraki-API-Key": API_KEY,
    "Content-Type": "application/json"
}

print("Connecting to Meraki API and fetching Organizations...")

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        orgs = response.json()
        print(f"\nFound {len(orgs)} Organization(s) associated with your account:")
        for org in orgs:
            # Display each Organization name and its unique ID
            print(f"- {org['name']} (ID: {org['id']})")
    else:
        print(f"API Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")