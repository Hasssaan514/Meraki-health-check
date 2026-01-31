import os
import meraki_health_check

API_KEY = os.getenv("MERAKI_API_KEY")

dashboard = meraki_health_check.DashboardAPI(API_KEY, suppress_logging=True)

orgs = dashboard.organizations.getOrganizations()

for org in orgs:
    print(f"Org Name: {org['name']} | Org ID: {org['id']}")
