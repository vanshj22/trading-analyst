import google.generativeai as genai
import os
from config import PRIMARY_MODEL

def test_key(key_source, key_value):
    print(f"\n--- Testing key from {key_source} ---")
    if not key_value:
        print("❌ No key found.")
        return

    # Mask key for display
    masked = key_value[:4] + "*" * (len(key_value)-8) + key_value[-4:] if len(key_value) > 10 else "****"
    print(f"Key: {masked}")
    
    try:
        genai.configure(api_key=key_value.strip())
        print("Attempting to list models...")
        models = list(genai.list_models())
        print(f"✅ Success! Found {len(models)} models.")
        
        print(f"Attempting generation with {PRIMARY_MODEL}...")
        model = genai.GenerativeModel(PRIMARY_MODEL)
        response = model.generate_content("Hello")
        print(f"✅ Generation successful: {response.text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

# 1. Test Env Var
env_key = os.getenv("GEMINI_API_KEY")
test_key("Environment Variable", env_key)

# 2. Test Manual Entry
# print("\n--- Manual Entry Test ---")
# manual_key = input("Paste your API Key here (press Enter to skip): ")
# if manual_key.strip():
#     test_key("Manual Input", manual_key)
