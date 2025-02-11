import requests

# SureMDM API URL of your account
url = "https://salling.eu.suremdm.io/api"
# Headers
headers = {
    # Api-Key header
    'ApiKey': "296A306B-B3BA-4719-9921-BA40CA5C690D",
    }
# Basic authentication credentials
Credentials=("avatorsinc@gmail.com","Add329ce34!")
# Send request
response = requests.put(url,auth=Credentials,headers=headers)
print(response)