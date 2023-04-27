import requests
url = 'http://127.0.0.1:8000/logout/'
headers = {'Authorization': 'Token <7c221e5371f614bc90ea5b0dd98de1d982ce571b>'}

response = requests.post(url, headers=headers)
print(response.status_code)
