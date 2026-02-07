import urllib.request
import json

url = "http://localhost:8000/api/trades/load-demo"
req = urllib.request.Request(url, method="POST")

try:
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        print(result)
except Exception as e:
    print(f"Error: {e}")
