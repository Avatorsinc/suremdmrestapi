import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

group_url = "https://salling.eu.suremdm.io/api/v2/group/082400110/getall"
assignment_url = "https://salling.eu.suremdm.io/api/v2/deviceassignment"

headers = {
    'ApiKey': "296A306B-B3BA-4719-9921-BA40CA5C690D",
    'Content-Type': "application/json",
}

email = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")
credentials = (email, password)

try:
    response = requests.get(group_url, auth=credentials, headers=headers)
    response.raise_for_status()
    raw_data = response.json()
    if isinstance(raw_data, dict) and "data" in raw_data:
        inner_data = raw_data["data"]
        if isinstance(inner_data, dict) and "Groups" in inner_data and isinstance(inner_data["Groups"], list):
            groups_list = inner_data["Groups"]
        else:
            print("Error: Unexpected data format in 'data'. Available keys:", list(inner_data.keys()))
            exit(1)
    else:
        print("Error: Unexpected API response format. 'data' key not found.")
        exit(1)
        
except requests.exceptions.RequestException as e:
    print("Error during group API request:", str(e))
    exit(1)
except json.JSONDecodeError as e:
    print("Error: Group API response is not valid JSON.", str(e))
    exit(1)

store_id = input("Enter Store ID (numbers only): ").strip()
search_prefix = f"Home/PDA/DK/Netto/{store_id} -"

matching_group = next(
    (group for group in groups_list 
     if isinstance(group, dict) and group.get("GroupPath", "").startswith(search_prefix)),
    None
)

if not matching_group:
    print(f"No matching group found for Store ID: {store_id}")
    exit(1)
group_id = matching_group.get("GroupID")
print(f"Found Group ID: {group_id} for Store ID: {store_id}")
device_id = input("Enter Device ID: ").strip()
assignment_payload = [
    {
        "DeviceId": device_id,
        "GroupId": group_id
    }
]
assignment_payload_json = json.dumps(assignment_payload)
try:
    assign_response = requests.put(assignment_url, auth=credentials, data=assignment_payload_json, headers=headers)
    assign_response.raise_for_status()
    print("Device assignment response: Device has been moved")
    print(assign_response.text)
except requests.exceptions.RequestException as e:
    print("Error during device assignment request:", str(e))
