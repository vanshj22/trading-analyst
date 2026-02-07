"""
Simple Example: Using Antifragile Mirror Programmatically
This script shows how to integrate the system into your own trading bot
"""
import os
from antifragile_controller import AntifragileController
import data_manager
import pandas as pd

def example_basic_usage():
    """Example 1: Basic setup and profiling"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Setup")
    print("=" * 60)
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Set GEMINI_API_KEY environment variable")
        return
    
    # Initialize controller
    controller = AntifragileController(api_key)
    
    # Load trade history (replace with your own CSV)
    trades_df = data_manager.generate_mock_trades(50)
    
    # Profile the trader
    profile = controller.initialize_trader_profile(trades_df)
    
    print(f"\n✅ Trader Profile:")
    print(f"   Win Rate: {profile['win_rate']}%")
    print(f"   Risk/Reward: {profile['risk_reward_ratio']}")
    print(f"   Dominant Bias: {profile['dominant_bias']}")
    print(f"   Revenge Signals: {profile['revenge_signals']}")

def example_monitor_trade():
    """Example 2: Monitor a single trade decision"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Monitor Trade Decision")
    print("=" * 60)
    
    api_key = os.getenv("GEMINI_API_KEY")
    controller = AntifragileController(api_key)
    trades_df = data_manager.generate_mock_trades(50)
    controller.initialize_trader_profile(trades_df)
    
    # Simulate: User wants to trade BTC after a loss
    print("\n📊 Scenario: User wants to trade BTC-USD")
    
    result = controller.run_cognitive_loop(
        ticker='BTC-USD',
        trades_df=trades_df,
        user_action='place_order'
    )
    
    # Check market conditions
    market = result['perception']['market']
    print(f"\n🌍 Market State:")
    print(f"   Price: ${market.get('current_price')}")
    print(f"   Regime: {market.get('regime')}")
    print(f"   Volatility: {market.get('volatility')}")
    
    # Check tilt score
    tilt = result['reasoning']['tilt']
    print(f"\n🧠 Tilt Analysis:")
    print(f"   Score: {tilt.get('tilt_score')}/10")
    print(f"   Requires Intervention: {tilt.get('requires_intervention')}")
    
    # Check intervention
    intervention = result['intervention']
    print(f"\n🎯 Intervention:")
    print(f"   Type: {intervention['type']}")
    
    if intervention['type'] != 'NONE':
        print(f"   Message: {intervention['message']}")
        
        # In a real bot, you would:
        if intervention['type'] == 'HARD_LOCK':
            print("\n   ⚠️ ACTION: Blocking trade execution")
            # block_trade()
        elif intervention['type'] == 'CRITICAL':
            print("\n   ⚠️ ACTION: Showing warning to user")
            # show_warning(intervention['message'])

def example_continuous_monitoring():
    """Example 3: Continuous monitoring loop"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Continuous Monitoring")
    print("=" * 60)
    
    api_key = os.getenv("GEMINI_API_KEY")
    controller = AntifragileController(api_key)
    trades_df = data_manager.generate_mock_trades(50)
    controller.initialize_trader_profile(trades_df)
    
    # Simulate multiple user actions
    actions = [
        ('check_position', 'AAPL'),
        ('place_order', 'TSLA'),
        ('cancel_order', 'TSLA'),
        ('place_order', 'TSLA'),  # Rapid re-entry
        ('cancel_order', 'TSLA'),
        ('place_order', 'BTC-USD'),  # Switching tickers rapidly
    ]
    
    print("\n🔄 Monitoring user actions...")
    
    for i, (action, ticker) in enumerate(actions, 1):
        print(f"\n--- Action {i}: {action} on {ticker} ---")
        
        result = controller.run_cognitive_loop(
            ticker=ticker,
            trades_df=trades_df,
            user_action=action
        )
        
        tilt_score = result['reasoning']['tilt'].get('tilt_score', 0)
        intervention_type = result['intervention']['type']
        
        print(f"Tilt Score: {tilt_score}/10 | Intervention: {intervention_type}")
        
        if intervention_type == 'HARD_LOCK':
            print("🚨 HARD LOCK TRIGGERED - Stopping monitoring")
            break

def example_custom_thresholds():
    """Example 4: Using custom thresholds"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Custom Thresholds")
    print("=" * 60)
    
    api_key = os.getenv("GEMINI_API_KEY")
    controller = AntifragileController(api_key)
    
    # Modify thresholds
    controller.tilt_detector.panic_threshold = 0.03  # More lenient
    
    print("\n⚙️ Custom Settings:")
    print(f"   Panic Threshold: {controller.tilt_detector.panic_threshold}")
    
    trades_df = data_manager.generate_mock_trades(50)
    controller.initialize_trader_profile(trades_df)
    
    result = controller.run_cognitive_loop('BTC-USD', trades_df)
    print(f"\n✅ System running with custom thresholds")

def example_diagnostics():
    """Example 5: System diagnostics"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: System Diagnostics")
    print("=" * 60)
    
    api_key = os.getenv("GEMINI_API_KEY")
    controller = AntifragileController(api_key)
    trades_df = data_manager.generate_mock_trades(50)
    controller.initialize_trader_profile(trades_df)
    
    # Run a few loops
    for _ in range(3):
        controller.run_cognitive_loop('AAPL', trades_df, 'check_position')
    
    # Get diagnostics
    diagnostics = controller.get_system_diagnostics()
    
    print("\n📊 System Diagnostics:")
    print(f"   Trader Profile: {diagnostics['trader_profile']['dominant_bias']}")
    print(f"   Total Interventions: {diagnostics['intervention_stats']['total']}")
    print(f"   User Interactions Tracked: {diagnostics['user_interaction_count']}")

def example_integration_pattern():
    """Example 6: Integration with existing trading bot"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Integration Pattern")
    print("=" * 60)
    
    print("""
    # Pseudo-code for integrating with your trading bot:
    
    class MyTradingBot:
        def __init__(self):
            self.antifragile = AntifragileController(api_key)
            self.trades_history = load_trades()
            self.antifragile.initialize_trader_profile(self.trades_history)
        
        def execute_trade(self, ticker, side, size):
            # Before executing, check with Antifragile Mirror
            result = self.antifragile.run_cognitive_loop(
                ticker=ticker,
                trades_df=self.trades_history,
                user_action='place_order'
            )
            
            intervention = result['intervention']
            
            if intervention['type'] == 'HARD_LOCK':
                print(f"🚨 Trade blocked: {intervention['message']}")
                return False
            
            elif intervention['type'] == 'CRITICAL':
                # Show warning but allow override
                user_confirms = ask_user_confirmation(intervention['message'])
                if not user_confirms:
                    return False
            
            # Execute trade
            return self.broker.place_order(ticker, side, size)
    """)

if __name__ == "__main__":
    print("\n🧠 ANTIFRAGILE MIRROR - USAGE EXAMPLES\n")
    
    # Run all examples
    try:
        example_basic_usage()
        example_monitor_trade()
        example_continuous_monitoring()
        example_custom_thresholds()
        example_diagnostics()
        example_integration_pattern()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure GEMINI_API_KEY is set:")
        print("  export GEMINI_API_KEY='your_key'")
