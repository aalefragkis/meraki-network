import requests
import json
import sys
from datetime import datetime

# 1. Load configuration from ignore_config.json
try:
    with open('ignore_config.json', 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print("Error: ignore_config.json file not found!")
    sys.exit()

# 2. Assign configuration variables
API_KEY = config['api_key']
ORG_ID = config['org_id']
NET_ID = config['network_id']
LOCATION = config['location']
ORG_NAME = config['org_name']

# API Endpoint for device statuses at the Organization level
url = f'https://api.meraki.com/api/v1/organizations/{ORG_ID}/devices/statuses'

headers = {
    'X-Cisco-Meraki-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

# Parameters to filter statuses for the specific network ID (e.g., JTR)
params = {'networkIds[]': [NET_ID]}

# Generate current timestamp for the report filename
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M")
filename = f"{LOCATION}_Health_Report_{timestamp}.txt"

print(f"Starting security audit for Organization: {ORG_NAME}...")
print(f"Generating report file: {filename}...")

try:
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        statuses = response.json()
        
        # Open a .txt file to write the security report
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"NETWORK HEALTH REPORT: {LOCATION} ({ORG_NAME})\n")
            file.write(f"Audit Date/Time: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("-" * 60 + "\n\n")
            
            offline_found = False
            for s in statuses:
                # Check for any status that is not 'online'
                if s.get('status') != 'online':
                    offline_found = True
                    # Log alerts for Offline or Dormant devices
                    line = f"[!] ALERT: {s.get('name', 'Unnamed')} | Status: {s.get('status').upper()} | MAC: {s.get('mac')}\n"
                    file.write(line)
            
            if not offline_found:
                file.write("All devices are Online. No issues detected.\n")
            
            file.write(f"\nSummary: Total of {len(statuses)} devices checked.")
            
        print(f"Report completed successfully! Total devices processed: {len(statuses)}")
        
    else:
        print(f"API Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"An error occurred during execution: {e}")