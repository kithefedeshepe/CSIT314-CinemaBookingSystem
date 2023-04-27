import requests

url = 'http://127.0.0.1:8000/changePW/'

response = requests.options(url)
if response.status_code == requests.codes.ok:
    allowed_methods = response.headers.get('Allow')
    print(f"The allowed methods for {url} are: {allowed_methods}")
else:
    print(f"Error: {response.status_code}")
