import os
import requests
from dotenv import load_dotenv

load_dotenv()
url = "https://salling.eu.suremdm.io/api/v2/group/gethomegroupdetails"
headers = {
    'ApiKey': "296A306B-B3BA-4719-9921-BA40CA5C690D",
    'Content-Type': "application/json",
}
email = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")
if not email or not password:
    raise ValueError("Chuj dupa cycki")
response = requests.get(url, auth=(email, password), headers=headers)
if response.status_code == 200:
    try:
        data = response.json()
        group_name = data.get('data', {}).get('TotalDevices')
        print(f"Total Devices: {group_name}")
    except ValueError:
        print("json error")
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")
