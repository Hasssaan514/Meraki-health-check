import os

# Function to get environment variable or prompt user
def get_env_var(var_name, prompt_message):
    value = os.getenv(var_name)
    if not value:
        print(f"{var_name} not found in environment variables.")
        value = input(f"Please enter {prompt_message}: ").strip()
        if not value:
            raise EnvironmentError(f"{var_name} is required to run this script.")
        # Optionally, set it for current session
        os.environ[var_name] = value
    return value

# Get Meraki Org ID
MERAKI_ORG_ID = get_env_var("MERAKI_ORG_ID", "Meraki Organization ID")

# Get Meraki API Key
MERAKI_API_KEY = get_env_var("MERAKI_API_KEY", "Meraki API Key")

# Now you can safely use MERAKI_ORG_ID and MERAKI_API_KEY
print(f"Using Organization ID: {MERAKI_ORG_ID}")
print(f"Using API Key: {'*' * len(MERAKI_API_KEY)}")  # mask API key for security

# --- Your Meraki health check code below ---
# Example:
# import meraki
# dashboard = meraki.DashboardAPI(MERAKI_API_KEY)
# networks = dashboard.organizations.getOrganizationNetworks(MERAKI_ORG_ID)
# print(networks)
