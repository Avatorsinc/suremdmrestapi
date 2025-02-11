import requests
import os
from dotenv import load_dotenv

load_dotenv()

DeviceId = "e379c33d-2258-4636-82b6-ef83b8b89940"

url = f"https://salling.eu.suremdm.io/api/v2/devicelog/{DeviceId}"

headers = {
    'ApiKey': "296A306B-B3BA-4719-9921-BA40CA5C690D",
    'Content-Type': "application/json",
}

username = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")

if not username or not password:
    raise ValueError("Username or password is missing.")

Credentials = (username, password)

response = requests.get(url, auth=Credentials, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")
