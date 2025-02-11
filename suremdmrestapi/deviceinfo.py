import requests

#SureMDM API URL of your account
url = "https://suremdm.42gears.com/api/v2/devicegrid"
#Add headers
headers = {
    #Api-Key header
    'ApiKey': "Your Api-Key",
    #Set content type
    'Content-Type': "application/json",
    }
#Basic authentication credentials
Credentials=("Username","Password")
#Payload
payload = "{  \"Limit\": 20,  \"Offset\": 0,  \"IsSearch\": true,  \"SearchValue\": \"\",  \"SortOrder\": \"asc\",  \"SortColumn\": \"DeviceName\"}"
#Send request
response = requests.post(url,auth=Credentials,data=payload,headers=headers)
print(response.text)
    
