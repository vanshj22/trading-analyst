import requests
import json
import time

def test_api():
    url = "http://127.0.0.1:8000/api/trades/load-demo"
    print(f"Testing {url}...")
    
    try:
        response = requests.post(url)
        if response.status_code == 200:
            data = response.json()
            print("Response received:")
            print(json.dumps(data, indent=2))
            
            trades = data.get("trades", [])
            if trades:
                first_trade = trades[0]
                expected_keys = ["timestamp", "ticker", "action", "quantity", "price", "PnL"]
                missing = [k for k in expected_keys if k not in first_trade]
                
                if not missing:
                    print("\nSUCCESS: All expected keys present!")
                else:
                    print(f"\nFAILURE: Missing keys: {missing}")
            else:
                print("\nWARNING: No trades returned")
        else:
            print(f"Error: Status code {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    # Give server a moment to start
    time.sleep(2)
    test_api()
