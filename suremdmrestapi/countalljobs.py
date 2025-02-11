import os
import requests
from dotenv import load_dotenv



load_dotenv()
url = "https://salling.eu.suremdm.io/api/v2/JobHistory/CountAllJobs/150ea75f-3065-4116-b083-c56a3f10396b"
headers = {
    'ApiKey': "296A306B-B3BA-4719-9921-BA40CA5C690D",
    'Content-Type': "application/json",
}

email = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")

if not email or not password:
    raise ValueError("Email or password missing")

response = requests.get(url, auth=(email, password), headers=headers)

if response.status_code == 200:
    try:
        data = response.json()
        if isinstance(data.get('data'), list) and len(data['data']) > 0:
            failed_jobs = data['data'][0].get('failed_jobs', 'N/A')
            deployed_jobs = data['data'][0].get('deployed_jobs', 'N/A')
            inprogres = data['data'][0].get('inprogres', 'N/A')
            scheduled = data['data'][0].get('scheduled', 'N/A')
            status = data['data'][0].get('status')
            print(f"Total deployed Jobs on device : {deployed_jobs}")
            print(f"Failed Jobs: {failed_jobs}")
            print(f"In progress Jobs : {inprogres}")
            print(f"All scheduled Jobs : {scheduled}")
        else:
            print("Data is empty or not in expected format.")
    except ValueError:
        print("Error parsing JSON response.")
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")



#EXAMPLE DATA 
# {"message":"Job status counts retrieved successfully","data":[{"deployed_jobs":"4","failed_jobs":"1","inprogres":"1","scheduled":"0","configured_scheduled_jobs":"0"}],"status":true}    