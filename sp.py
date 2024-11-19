import yaml
import subprocess

# Load service principal data from YAML
with open('config.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Define role, subscription, and scope
role = "Contributor"
scope = "/subscriptions/b282c457-292d-4181-96a4-169ac357585a/resourceGroups/OliviaAI_group/providers/Microsoft.Quantum/workspaces/OliviaAIQuantum"
subprocess.run([
    r"C:\Program Files (x86)\Microsoft SDKs\Azure\bin\az.cmd",  # Full path to az executable
    "role", "assignment", "create",
    sp_id = config.get("id") # Replace with the correct service principal ID
    role = "Contributor"  # Define the role
    scope = "/subscriptions/b282c457-292d-4181-96a4-169ac357585a/resourceGroups/OliviaAI_group/providers/Microsoft.Quantum/workspaces/OliviaAIQuantum"
], check=True)

# Iterate over each service principal and assign the role
for sp in data["service_principals"]:
    sp_id = sp["id"]
    sp_name = sp["name"]

    print(f"Assigning role '{role}' to service principal '{sp_name}' (ID: {sp_id})...")

    try:
        # Run the Azure CLI command to create the role assignment
        subprocess.run([
            "az", "role", "assignment", "create",
            "--assignee", sp_id,
            "--role", role,
            "--scope", scope
        ], check=True)
        print(f"Successfully assigned role to {sp_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to assign role to {sp_name}: {e}")
