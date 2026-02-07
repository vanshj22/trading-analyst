import requests
import sys

try:
    print("Testing backend on port 8001...")
    response = requests.get("http://localhost:8001/docs")
    if response.status_code == 200:
        print("SUCCESS: Backend is responding on port 8001")
        
        # Check trades endpoint
        trades_response = requests.get("http://localhost:8001/api/trades")
        if trades_response.status_code == 200:
            print(f"SUCCESS: Trades endpoint working. Count: {trades_response.json().get('count', 0)}")
        else:
            print(f"FAILURE: Trades endpoint returned status {trades_response.status_code}")
            print(trades_response.text)
            
    else:
        print(f"FAILURE: Backend returned status {response.status_code}")
except Exception as e:
    print(f"EXCEPTION: Connection failed: {e}")
