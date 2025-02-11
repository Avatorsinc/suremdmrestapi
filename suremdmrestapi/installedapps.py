import requests
import os
from dotenv import load_dotenv
load_dotenv()
url = "https://salling.eu.suremdm.io/api/v2/installedapp/android/62c2eba0-ed18-436b-82c8-32fa33b2394b/device/50/1/android/name/asc/android"
headers = {
    'ApiKey': "e379c33d-2258-4636-82b6-ef83b8b89940",
    'Content-Type': "application/json",
    }

#username = os.getenv("MY_EMAIL")
#password = os.getenv("MY_PASSWORD")
Credentials = ("avatorsinc@gmail.com", "Add329ce34!")

#if not username or not password:
    #raise ValueError("Username or password is missing.")

#print(Credentials)
response = requests.get(url, auth=Credentials, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")
