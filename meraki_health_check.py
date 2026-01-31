import os
import csv
from dotenv import load_dotenv
import meraki
 
# -----------------------
# Load environment variables
# -----------------------
load_dotenv()  # loads .env file if present
 
def get_env_var(var_name, prompt_message):
    """Get environment variable or prompt user to enter it"""
    value = os.getenv(var_name)
    if not value:
        print(f"\n{var_name} not found in environment variables.")
        value = input(f"Please enter {prompt_message}: ").strip()
        if not value:
            raise EnvironmentError(f"{var_name} is required to run this script.")
        os.environ[var_name] = value  # set for current session
    return value
 
# Get API key and Org ID
API_KEY = get_env_var("MERAKI_API_KEY", "Meraki API Key")
ORG_ID = get_env_var("MERAKI_ORG_ID", "Meraki Organization ID")
 
print(f"\nUsing Organization ID: {ORG_ID}")
print(f"Using API Key: {'*' * len(API_KEY)}")  # mask API key
 
# -----------------------
# Connect to Meraki Dashboard
# -----------------------
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)
 
# -----------------------
# Validate API key by fetching networks
# -----------------------
try:
    networks = dashboard.organizations.getOrganizationNetworks(ORG_ID)
    print(f"Successfully connected! Found {len(networks)} networks.")
except meraki.exceptions.APIError as e:
    raise SystemExit(f"Error connecting to Meraki API: {e}")
 
# -----------------------
# Collect device info for report
# -----------------------
report_data = []
 
for network in networks:
    network_id = network["id"]
    network_name = network["name"]
 
    try:
        devices = dashboard.networks.getNetworkDevices(network_id)
    except meraki.exceptions.APIError as e:
        print(f"Warning: Could not fetch devices for network {network_name} ({network_id}): {e}")
        continue
 
    for device in devices:
        report_data.append({
            "Network Name": network_name,
            "Device Name": device.get("name", "N/A"),
            "Model": device.get("model", "N/A"),
            "Serial": device.get("serial", "N/A"),
            "Status": device.get("status", device.get("reachability", "Unknown")),
            "LAN IP": device.get("lanIp", device.get("wan1Ip", "N/A")),
            "Public IP": device.get("publicIp", device.get("wan1Ip", "N/A"))
        })
 
# -----------------------
# Write report to CSV
# -----------------------
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)
csv_file = os.path.join(output_folder, "meraki_report.csv")
 
if report_data:
    with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = report_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_data)
    print(f"Meraki health report generated successfully! Check {csv_file}")
else:
    print("No device data found. The report was not generated.")