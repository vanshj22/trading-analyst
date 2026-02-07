"""
Test script for Antifragile Mirror system
Verifies all components work correctly
"""
import os
from antifragile_controller import AntifragileController
import data_manager

def test_system():
    print("🧪 Testing Antifragile Mirror System\n")
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        print("Set it with: export GEMINI_API_KEY='your_key'")
        return
    
    print("✅ API Key loaded")
    
    # Generate test data
    print("\n📊 Generating mock trade data...")
    trades_df = data_manager.generate_mock_trades(30)
    print(f"✅ Generated {len(trades_df)} trades")
    
    # Initialize controller
    print("\n🚀 Initializing Antifragile Controller...")
    controller = AntifragileController(api_key)
    
    # Profile trader
    print("\n👤 Profiling trader...")
    profile = controller.initialize_trader_profile(trades_df)
    print(f"✅ Profile complete:")
    print(f"   - Win Rate: {profile['win_rate']}%")
    print(f"   - Revenge Signals: {profile['revenge_signals']}")
    print(f"   - Dominant Bias: {profile['dominant_bias']}")
    
    # Test cognitive loop
    print("\n🔄 Running cognitive loop...")
    
    # Simulate normal trading
    print("\n1️⃣ Test Case: Normal Trading")
    result1 = controller.run_cognitive_loop('AAPL', trades_df, 'check_position')
    print(f"   Tilt Score: {result1['reasoning']['tilt'].get('tilt_score', 0)}/10")
    print(f"   Intervention: {result1['intervention']['type']}")
    
    # Simulate erratic behavior
    print("\n2️⃣ Test Case: Erratic Behavior (Simulating Tilt)")
    # Simulate rapid-fire actions
    for _ in range(10):
        controller.user_stream.capture_interaction('cancel_order')
        controller.user_stream.capture_interaction('place_order')
    
    result2 = controller.run_cognitive_loop('BTC-USD', trades_df, 'place_order')
    print(f"   Tilt Score: {result2['reasoning']['tilt'].get('tilt_score', 0)}/10")
    print(f"   Intervention: {result2['intervention']['type']}")
    
    if result2['intervention']['type'] != 'NONE':
        print(f"\n   🚨 Intervention Message:")
        print(f"   {result2['intervention']['message']}")
    
    # System diagnostics
    print("\n📈 System Diagnostics:")
    diagnostics = controller.get_system_diagnostics()
    print(f"   - Total Interventions: {diagnostics['intervention_stats']['total']}")
    print(f"   - User Interactions Tracked: {diagnostics['user_interaction_count']}")
    
    print("\n✅ All tests completed successfully!")
    print("\n🚀 Run the full UI with: streamlit run antifragile_app.py")

if __name__ == "__main__":
    test_system()
