import google.generativeai as genai
import os
from dotenv import load_dotenv
import sys

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

print("--- Listing Available Models ---")
try:
    for m in genai.list_models():
        print(f"Name: {m.name}")
        print(f"Supported methods: {m.supported_generation_methods}")
        print("-" * 20)
except Exception as e:
    print(f"Error listing models: {e}")

print("\n--- Testing Specific Models ---")
models_to_test = ["gemini-pro", "gemini-1.5-flash", "gemini-1.0-pro", "gemini-1.5-pro"]

for model_name in models_to_test:
    print(f"Testing {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Test")
        print(f"SUCCESS: {model_name} works!")
        break # Found a working one
    except Exception as e:
        print(f"FAILED: {model_name} - {str(e)[:100]}...")
