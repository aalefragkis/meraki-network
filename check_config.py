import requests
import json
import sys

def validate_config():
    print("--- Starting Configuration Check ---")
    
    # 1. Check if the file exists and is valid JSON
    try:
        with open('ignore_config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)
            print("[OK] ignore_config.json found and parsed successfully.")
    except FileNotFoundError:
        print("[ERROR] ignore_config.json file is missing!")
        return False
    except json.JSONDecodeError:
        print("[ERROR] Syntax error in ignore_config.json (check for missing commas!).")
        return False

    # 2. Check for required configuration keys
    required_keys = ['api_key', 'org_id']
    for key in required_keys:
        if key not in config:
            print(f"[ERROR] Missing configuration key: {key}")
            return False

    # 3. Verify API Key validity with Meraki Cloud
    print("Verifying API Key with Meraki API...")
    url = "https://api.meraki.com/api/v1/organizations"
    headers = {
        "X-Cisco-Meraki-API-Key": config['api_key'],
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("[SUCCESS] API Key is valid! Connection established.")
            return True
        elif response.status_code == 401:
            print("[ERROR] Invalid API Key (401 Unauthorized).")
            return False
        else:
            print(f"[ERROR] Something went wrong. Status Code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network problem: {e}")
        return False

# Execute validation
if __name__ == "__main__":
    if validate_config():
        print("\nAll checks passed! You are ready to run your scripts.")
    else:
        print("\nPlease fix the errors above before proceeding.")
        sys.exit(1)