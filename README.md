# Meraki Health Check

Python-based health check script for Cisco Meraki networks.
The script connects to the Meraki Dashboard API, validates access,
and generates a CSV report of device health and IP information.

## Features
- Secure API key handling using environment variables
- Organization-based network discovery
- Device inventory and health status
- CSV report generation

## Project Files
- meraki_health_check.py → Main script
- get_orgs.py → Organization discovery helper
- test_meraki.py → API connectivity testing
- env_test.py → Environment variable testing

## Requirements
- Python 3.8+
- Meraki Dashboard API access

## Installation
```bash
pip install -r requirements.txt
