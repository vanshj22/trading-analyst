"""
Cognitive Layer: Multi-Agent Brain
Three specialized agents: Market Analyst, Profiler, Tilt Detector
"""
import numpy as np
from typing import Dict, List
import google.generativeai as genai

class MarketAnalystAgent:
    """Identifies regime shifts and market anomalies"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
    
    def analyze_regime(self, market_state: Dict) -> Dict:
        """Detects if market entered a new regime"""
        prompt = f"""You are a market regime analyst. Analyze this market state:

Ticker: {market_state.get('ticker')}
Volatility: {market_state.get('volatility')}
Regime: {market_state.get('regime')}
Price Change (5d): {market_state.get('price_change_5d')}%
Volume Spike: {market_state.get('volume_spike')}

Respond in JSON format:
{{
  "regime_type": "LOW_VOL|HIGH_VOL|CRISIS",
  "risk_level": "LOW|MEDIUM|HIGH|EXTREME",
  "trader_advice": "brief advice"
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            return {'analysis': response.text, 'raw_state': market_state}
        except Exception as e:
            return {'error': str(e)}

class ProfilerAgent:
    """Vectorizes user's trading history to identify latent biases"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        self.bias_patterns = {}
    
    def profile_trader(self, trades_df) -> Dict:
        """Identifies psychological biases from trade history"""
        if trades_df.empty:
            return {'error': 'No trades to analyze'}
        
        # Calculate key metrics
        total_trades = len(trades_df)
        win_rate = len(trades_df[trades_df['PnL'] > 0]) / total_trades
        avg_win = trades_df[trades_df['PnL'] > 0]['PnL'].mean() if any(trades_df['PnL'] > 0) else 0
        avg_loss = trades_df[trades_df['PnL'] < 0]['PnL'].mean() if any(trades_df['PnL'] < 0) else 0
        
        # Detect revenge trading pattern
        pnl_sequence = trades_df['PnL'].tolist()
        revenge_signals = 0
        for i in range(1, len(pnl_sequence)):
            if pnl_sequence[i-1] < -100 and pnl_sequence[i] < 0:
                revenge_signals += 1
        
        # Check for FOMO in notes
        fomo_count = trades_df['Trade Note'].str.contains('FOMO|Revenge', case=False, na=False).sum()
        
        profile = {
            'total_trades': total_trades,
            'win_rate': round(win_rate * 100, 1),
            'avg_win': round(avg_win, 2),
            'avg_loss': round(avg_loss, 2),
            'revenge_signals': revenge_signals,
            'fomo_trades': int(fomo_count),
            'risk_reward_ratio': round(abs(avg_win / avg_loss), 2) if avg_loss != 0 else 0
        }
        
        # Store for pattern matching
        self.bias_patterns = profile
        return profile
    
    def detect_bias_type(self, profile: Dict) -> str:
        """Classifies dominant bias"""
        if profile['revenge_signals'] > 2:
            return "LOSS_AVERSION_REVENGE"
        elif profile['fomo_trades'] > 3:
            return "FOMO_OVERTRADING"
        elif profile['win_rate'] < 40:
            return "POOR_EDGE_EXECUTION"
        elif profile['risk_reward_ratio'] < 1.5:
            return "CUTTING_WINNERS_EARLY"
        else:
            return "DISCIPLINED_TRADER"

class TiltDetectorAgent:
    """Compares live volatility against user's panic threshold"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        self.panic_threshold = 0.025  # Default 2.5% volatility
    
    def detect_tilt(self, market_state: Dict, user_behavior: Dict, trader_profile: Dict) -> Dict:
        """Chain-of-Thought reasoning to detect tilt state"""
        
        # Rule-based pre-check
        is_high_vol = market_state.get('regime') == 'HIGH_VOL'
        is_erratic = user_behavior.get('is_erratic', False)
        has_revenge_history = trader_profile.get('revenge_signals', 0) > 2
        
        tilt_score = 0
        if is_high_vol:
            tilt_score += 3
        if is_erratic:
            tilt_score += 4
        if has_revenge_history:
            tilt_score += 2
        
        # LLM reasoning for complex cases
        if tilt_score >= 5:
            prompt = f"""You are a trading psychology expert. Analyze this situation:

MARKET: {market_state.get('regime')} regime, volatility {market_state.get('volatility')}
USER BEHAVIOR: {user_behavior.get('total_actions')} actions in 5min, {user_behavior.get('cancel_count')} cancels
TRADER HISTORY: {trader_profile.get('revenge_signals')} revenge patterns detected

Is the trader in TILT? Respond in JSON:
{{
  "tilt_detected": true/false,
  "severity": "LOW|MEDIUM|HIGH|CRITICAL",
  "reasoning": "brief explanation",
  "trigger": "what caused it"
}}"""
            
            try:
                response = self.model.generate_content(prompt)
                return {
                    'tilt_score': tilt_score,
                    'llm_analysis': response.text,
                    'requires_intervention': tilt_score >= 7
                }
            except Exception as e:
                return {'error': str(e)}
        
        return {
            'tilt_score': tilt_score,
            'tilt_detected': False,
            'requires_intervention': False
        }
