import requests       
url = 'http://127.0.0.1:8000/logout/'
headers = {'Authorization': 'Token <7ef3b0ddbecb5f20a919d4631929600a351a0aca>'}

response = requests.post(url, headers=headers)
print(response.status_code)