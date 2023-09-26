import requests
import sys
import json
import subprocess
import datetime
import os
import base64
import time

# Replace these placeholders with your actual values
tenant_id = sys.argv[1]
client_id = sys.argv[2]
client_secret = sys.argv[3]
group_id = sys.argv[4]
work_dir = sys.argv[5]
pat = sys.argv[6]

# Obtain an access token using the client credentials flow
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "resource": "https://analysis.windows.net/powerbi/api",
}
token_response = requests.post(token_url, data=token_data)

if token_response.status_code == 200:
    access_token = token_response.json()["access_token"]
    print("Fetch Access Token successful")
else:
    print(f"Error obtaining access token: {token_response.status_code}: {token_response.text}")
    exit(1)

# Call the Power BI REST API using the access token
headers = {
    "Authorization": f"Bearer {access_token}",
}

if group_id is None or group_id == "": # If no group id is provided, get all workspaces
    # Get all workspaces
    workspaces_url = f"https://api.powerbi.com/v1.0/myorg/admin/groups?$top=1000&$filter=type eq 'Workspace'"
    get_workspaces_response = requests.get(workspaces_url, headers=headers)

    if get_workspaces_response.status_code == 200 or get_workspaces_response.status_code == 202:
        print(json.dumps(get_workspaces_response.json(), indent=3))
    else:
        print(f"Error in API request: {get_workspaces_response.status_code}: {get_workspaces_response.text}")
        exit(1)

    workspaces_ids = [item['id'] for item in get_workspaces_response.json()['value']]
else:
    workspaces_ids = [group_id]

workspace_chunks = [workspaces_ids[i:i+100] for i in range(0, len(workspaces_ids), 100)]

chunk_index = 1
for chunk in workspace_chunks:
    # Start the scan
    start_scan_url = f"https://api.powerbi.com/v1.0/myorg/admin/workspaces/getInfo?lineage=True&datasourceDetails=True&datasetSchema=True&datasetExpressions=True&getArtifactUsers=True"
    workspaces = {
        "workspaces": chunk
    }

    scan_start_response = requests.post(start_scan_url, headers=headers, data=workspaces)

    if scan_start_response.status_code == 200 or scan_start_response.status_code == 202:
        print(json.dumps(scan_start_response.json(), indent=3))
    else:
        print(f"Error in API request: {scan_start_response.status_code}: {scan_start_response.text}")

    scan_start_data = scan_start_response.json()
    scan_id = scan_start_data["id"]
    scan_status = scan_start_data["status"]

    scan_status_url = f"https://api.powerbi.com/v1.0/myorg/admin/workspaces/scanStatus/{scan_id}"

    while scan_status != "Succeeded":
        print(f"Scan status is {scan_status}. Waiting for scan to complete...")
        scan_status_response = requests.get(scan_status_url, headers=headers)
        if scan_status_response.status_code == 200:
            scan_status_data = scan_status_response.json()
            scan_status = scan_status_data["status"]
            print(json.dumps(scan_status_response.json(), indent=3))
        else:
            print(f"Error in API request: {scan_status_response.status_code}: {scan_status_response.text}")
            #exit(1)
        time.sleep(2)

    scan_result_url = f"https://api.powerbi.com/v1.0/myorg/admin/workspaces/scanResult/{scan_id}"
    scan_result_response = requests.get(scan_result_url, headers=headers)

    if scan_result_response.status_code == 200:
        print(json.dumps(scan_result_response.json(), indent=3))
    else:
        print(f"Error in API request: {scan_result_response.status_code}: {scan_result_response.text}")

    data = scan_result_response.json()
    data["lastScanDate"] = datetime.datetime.now().strftime('%B %d, %Y %H:%M:%S')

    directory = 'export'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(work_dir, directory,f'scanResult-{ chunk_index }.json')
    chunk_index += 1
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    while not os.path.exists(file_path):
        print(f"Waiting for file {file_path} to be created...")
        time.sleep(1)

# Get the current date and time in the specified format
current_date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')

# Get the PAT
if pat is None:
    print("PAT environment variable not found.")
    exit(1)

# Encode the PAT in base64
b64_pat = base64.b64encode(f":{pat}".encode()).decode()
branch_name = f"api-{current_date}"
# Run the git commands with the encoded PAT
try:
    subprocess.run(["git", "config", "--global", "user.email", "azure-pipeline@coso.com"], check=True)
    subprocess.run(["git", "config", "--global", "user.name", "Azure Pipeline"], check=True)
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    subprocess.run(["git", "-c", f"http.extraHeader=Authorization: Basic {b64_pat}", "add", "."], check=True)
    subprocess.run(["git", "-c", f"http.extraHeader=Authorization: Basic {b64_pat}", "commit", "-m", "API Import"], check=True)
    subprocess.run(["git", "-c", f"http.extraHeader=Authorization: Basic {b64_pat}", "push", "--set-upstream", "origin", branch_name ], check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred during Git operations: {str(e)}")

