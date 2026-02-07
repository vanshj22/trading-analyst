"""
Example: Integrating Real Mouse Tracking with Antifragile Mirror
Install: pip install pynput
"""
import os
from antifragile_controller import AntifragileController
from mouse_tracker import MouseSpeedTracker
import data_manager
import time

def example_with_mouse_tracking():
    """Run Antifragile Mirror with real mouse speed tracking"""
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Set GEMINI_API_KEY environment variable")
        return
    
    # Initialize system
    controller = AntifragileController(api_key)
    trades_df = data_manager.generate_mock_trades(50)
    controller.initialize_trader_profile(trades_df)
    
    # Start mouse tracking
    mouse_tracker = MouseSpeedTracker()
    mouse_tracker.start_tracking()
    
    print("\n=== Mouse Tracking Active ===")
    print("Move your mouse around to simulate trading activity...")
    print("Fast movements = panic indicator\n")
    
    try:
        # Monitor for 30 seconds
        for i in range(6):
            time.sleep(5)
            
            # Get current mouse speed
            avg_speed = mouse_tracker.get_average_speed()
            
            # Feed mouse speed to controller
            controller.user_stream.capture_mouse_speed(avg_speed)
            
            # Simulate some trading actions
            if avg_speed > 300:  # Fast movement
                controller.user_stream.capture_interaction('place_order')
                controller.user_stream.capture_interaction('cancel_order')
            
            # Run cognitive loop
            result = controller.run_cognitive_loop('BTC-USD', trades_df)
            
            # Display results
            print(f"\n--- Check {i+1}/6 ---")
            print(f"Mouse Speed: {avg_speed:.2f} px/sec")
            print(f"Tilt Score: {result['reasoning']['tilt'].get('tilt_score', 0)}/10")
            print(f"Intervention: {result['intervention']['type']}")
            
            if result['intervention']['type'] != 'NONE':
                print(f"\nWARNING: {result['intervention']['message'][:100]}...")
    
    finally:
        mouse_tracker.stop_tracking()
        print("\n=== Tracking Stopped ===")

if __name__ == "__main__":
    example_with_mouse_tracking()
