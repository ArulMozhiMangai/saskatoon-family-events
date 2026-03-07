import requests
url = "https://saskatoonlibrary.libnet.info/events?r=tomorrow"
response = requests.get(url)
print(response.status_code)
print(response.text[:500])