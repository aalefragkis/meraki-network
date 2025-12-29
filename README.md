# meraki-network
Meraki Network monitoring tools.

# Meraki Network Management Suite

A collection of Python scripts designed for automated management, security auditing, and health monitoring of Cisco Meraki networks, specifically optimized for airport infrastructure environments.

## 🛠 Features

- **Automated Security Audits**: Detect unauthorized devices in real-time.
- **Health Reporting**: Generate automated status reports for network inventory.
- **Organization Management**: Efficiently list and manage multiple organizations and networks.
- **Security-First Design**: Uses external configuration files and `.gitignore` to protect sensitive API credentials.

## 📂 Project Structure

- `check_config.py`: Validates the integrity of the configuration and API connectivity.
- `intruder_detector.py`: Scans for devices not present in the authorized whitelist.
- `meraki_security_report.py`: Generates a timestamped health report in `.txt` format.
- `get_org_networks.py`: Retrieves all networks associated with a specific Organization ID.
- `meraki_devices.py`: Lists all hardware assets with their MAC addresses and models.

## 🚀 Setup & Installation

1. **Clone the repository**:

```bash
   git clone https://github.com/aalefragkis/meraki-network.git
   cd meraki-network
```

2. **Configuration**:
Copy the provided sample configuration file to create your local config:

```bash
   cp sample_ignore_config.json ignore_config.json
```


3. **Run the Pre-flight Check**:

```bash
python3 check_config.py
```



## 🛡 Security Note

This project follows security best practices by ensuring that no API keys or sensitive organizational data are ever committed to the version control system.

---

**Developed for Network Engineering & Cyber Security monitoring.**

*Antonios Alefragkis, Greece*
