  import requests
  url = "https://salling.eu.suremdm.io/api/v2/devicename"
  headers = {
      'ApiKey': "296A306B-B3BA-4719-9921-BA40CA5C690D",
      }
  Credentials=("Username","Password")
  response = requests.put(url,auth=Credentials,headers=headers)