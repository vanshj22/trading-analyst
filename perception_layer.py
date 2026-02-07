"""
Perception Layer: Sensory Input for the Antifragile Mirror
Ingests Market Stream + User Behavioral Stream
"""
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List

class MarketStreamProcessor:
    """Processes real-time market data and detects regime shifts"""
    
    def __init__(self):
        self.volatility_threshold = 0.02  # 2% for regime detection
        
    def capture_market_state(self, ticker: str) -> Dict:
        """Captures current market conditions"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d", interval="1h")
            
            if hist.empty or len(hist) < 2:
                # No data available from yfinance, use demo data
                raise Exception("No historical data available")
            
            # Calculate volatility (std of returns)
            returns = hist['Close'].pct_change().dropna()
            volatility = returns.std()
            
            # Detect regime
            regime = "HIGH_VOL" if volatility > self.volatility_threshold else "LOW_VOL"
            
            # Price momentum
            price_change = (hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]
            
            return {
                'ticker': ticker,
                'current_price': round(hist['Close'].iloc[-1], 2),
                'volatility': round(volatility, 4),
                'regime': regime,
                'price_change_5d': round(price_change * 100, 2),
                'volume_spike': hist['Volume'].iloc[-1] > hist['Volume'].mean() * 1.5,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            # Fallback to demo data if live data fails
            import random
            print(f"Market Stream Error: {e}. Using demo data.")
            
            base_price = 150.0
            volatility = random.uniform(0.01, 0.05)
            
            return {
                'ticker': ticker,
                'current_price': round(base_price * (1 + random.uniform(-0.05, 0.05)), 2),
                'volatility': round(volatility, 4),
                'regime': "HIGH_VOL" if volatility > self.volatility_threshold else "LOW_VOL",
                'price_change_5d': round(random.uniform(-5, 5), 2),
                'volume_spike': random.choice([True, False]),
                'timestamp': datetime.now().isoformat(),
                'is_demo': True
            }

class UserStreamProcessor:
    """Processes user behavioral data - interaction patterns"""
    
    def __init__(self):
        self.interaction_buffer = []
        self.mouse_speed_buffer = []  # NEW: Store mouse speeds
        
    def capture_interaction(self, action_type: str, metadata: Dict = None):
        """Logs user interaction events"""
        event = {
            'timestamp': datetime.now(),
            'action': action_type,
            'metadata': metadata or {}
        }
        self.interaction_buffer.append(event)
        
        # Keep only last 100 events
        if len(self.interaction_buffer) > 100:
            self.interaction_buffer.pop(0)
    
    def capture_mouse_speed(self, speed: float):
        """NEW: Logs mouse movement speed"""
        self.mouse_speed_buffer.append({
            'timestamp': datetime.now(),
            'speed': speed
        })
        
        # Keep only last 50 speeds
        if len(self.mouse_speed_buffer) > 50:
            self.mouse_speed_buffer.pop(0)
    
    def analyze_interaction_velocity(self, window_minutes: int = 5) -> Dict:
        """Detects rapid-fire behavior (panic indicator)"""
        cutoff = datetime.now() - timedelta(minutes=window_minutes)
        recent = [e for e in self.interaction_buffer if e['timestamp'] > cutoff]
        
        action_counts = {}
        for event in recent:
            action = event['action']
            action_counts[action] = action_counts.get(action, 0) + 1
        
        # Detect erratic patterns
        cancel_rate = action_counts.get('cancel_order', 0)
        order_rate = action_counts.get('place_order', 0)
        
        # NEW: Check mouse speed
        recent_mouse = [m for m in self.mouse_speed_buffer 
                       if m['timestamp'] > cutoff]
        avg_mouse_speed = sum(m['speed'] for m in recent_mouse) / len(recent_mouse) if recent_mouse else 0
        
        is_erratic = cancel_rate > 3 or order_rate > 5 or avg_mouse_speed > 500
        
        return {
            'total_actions': len(recent),
            'cancel_count': cancel_rate,
            'order_count': order_rate,
            'avg_mouse_speed': round(avg_mouse_speed, 2),  # NEW
            'is_erratic': is_erratic,
            'velocity_score': len(recent) / max(window_minutes, 1)
        }
    
    def get_recent_pnl_sequence(self, trades_df) -> List[float]:
        """Extracts recent PnL sequence for pattern matching"""
        if trades_df.empty:
            return []
        return trades_df.tail(10)['PnL'].tolist()
