import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.getcwd())

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in environment")
    sys.exit(1)

try:
    from persona_bot import PersonaBot
    print("Initializing PersonaBot...")
    bot = PersonaBot(api_key)
    
    print("Generating test tweet...")
    content = bot.generate_twitter_post(
        "The Quantitative Stoic", 
        "Market volatility", 
        "VIX is up 5%"
    )
    
    if "Error" in content:
        print(f"FAILED: {content}")
    else:
        print(f"SUCCESS: Generated content:\n{content}")
        
except Exception as e:
    print(f"EXCEPTION: {e}")
