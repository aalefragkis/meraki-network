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

# 2. Assign variables from configuration
API_KEY = config['api_key']
NET_ID = config['network_id']
LOCATION = config['location']
WHITELIST = config.get('whitelist', [])

# Meraki endpoint for network clients
url = f'https://api.meraki.com/api/v1/networks/{NET_ID}/clients'

headers = {
    'X-Cisco-Meraki-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

print(f"--- User Security Audit: {LOCATION} ---")
print("Scanning for unauthorized devices (last 15 minutes)...")

try:
    # Parameter 'timespan' set to 900 seconds (15 minutes)
    params = {'timespan': 900}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        clients = response.json()
        intruders_found = 0
        
        # Convert whitelist to lowercase for case-insensitive comparison
        safe_whitelist = [m.lower() for m in WHITELIST]
        
        print(f"\nTotal connected devices: {len(clients)}")
        print("-" * 50)
        
        for client in clients:
            mac = client.get('mac').lower()
            description = client.get('description', 'Unknown Device')
            
            # Check if the MAC address is NOT in the whitelist
            if mac not in safe_whitelist:
                intruders_found += 1
                print(f"[SECURITY ALERT] Unauthorized Device Detected!")
                print(f"Description: {description}")
                print(f"MAC: {mac} | IP: {client.get('ip', 'N/A')}")
                print(f"Connected to AP: {client.get('recentDeviceName', 'N/A')}")
                print("-" * 30)
        
        if intruders_found == 0:
            print("Result: All devices are whitelisted. Network is secure.")
        else:
            print(f"SUMMARY: Found {intruders_found} unauthorized device(s).")
            
    else:
        print(f"API Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"An error occurred during scanning: {e}")