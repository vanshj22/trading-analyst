import os
from dotenv import load_dotenv
from action_layer import InterventionEngine

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
    exit(1)

try:
    print("Initializing InterventionEngine...")
    engine = InterventionEngine(api_key)
    
    # Mock data for testing
    tilt_analysis = {'tilt_score': 8, 'requires_intervention': True, 'llm_analysis': 'Trader is showing signs of frustration.'}
    trader_profile = {'win_rate': 45, 'revenge_signals': 2}
    market_state = {'regime': 'Volatile'}
    
    print("Generating intervention...")
    intervention = engine.generate_intervention(tilt_analysis, trader_profile, market_state)
    
    print("\nIntervention Result:")
    print(intervention)
    
    if intervention['type'] != 'ERROR':
        print("\nSUCCESS: Intervention generated successfully.")
    else:
        print("\nFAILURE: Intervention generation failed.")

except Exception as e:
    print(f"\nEXCEPTION: {e}")
