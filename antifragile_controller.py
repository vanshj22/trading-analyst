"""
Orchestration Layer: Lead Controller
Coordinates the Perceive-Reason-Intervene loop across all agents
"""
from perception_layer import MarketStreamProcessor, UserStreamProcessor
from cognitive_layer import MarketAnalystAgent, ProfilerAgent, TiltDetectorAgent
from action_layer import InterventionEngine
from typing import Dict
import pandas as pd

class AntifragileController:
    """
    Lead Controller for the Antifragile Mirror System
    Orchestrates the cognitive loop: Perceive → Reason → Intervene
    """
    
    def __init__(self, api_key: str):
        # Perception Layer
        self.market_stream = MarketStreamProcessor()
        self.user_stream = UserStreamProcessor()
        
        # Cognitive Layer
        self.market_analyst = MarketAnalystAgent(api_key)
        self.profiler = ProfilerAgent(api_key)
        self.tilt_detector = TiltDetectorAgent(api_key)
        
        # Action Layer
        self.intervention_engine = InterventionEngine(api_key)
        
        # System state
        self.trader_profile = {}
        self.current_market_state = {}
        self.system_active = True
    
    def initialize_trader_profile(self, trades_df: pd.DataFrame):
        """One-time profiling of trader's historical behavior"""
        print("Initializing trader profile...")
        self.trader_profile = self.profiler.profile_trader(trades_df)
        bias_type = self.profiler.detect_bias_type(self.trader_profile)
        self.trader_profile['dominant_bias'] = bias_type
        print(f"Profile complete. Dominant bias: {bias_type}")
        return self.trader_profile
    
    def perceive(self, ticker: str, user_action: str = None, action_metadata: Dict = None):
        """
        PERCEIVE: Capture market + user state
        """
        # Market perception
        self.current_market_state = self.market_stream.capture_market_state(ticker)
        
        # User perception
        if user_action:
            self.user_stream.capture_interaction(user_action, action_metadata)
        
        user_behavior = self.user_stream.analyze_interaction_velocity()
        
        return {
            'market': self.current_market_state,
            'user': user_behavior
        }
    
    def reason(self, perception: Dict) -> Dict:
        """
        REASON: Multi-agent analysis
        """
        market_state = perception['market']
        user_behavior = perception['user']
        
        # Agent 1: Market Analyst
        regime_analysis = self.market_analyst.analyze_regime(market_state)
        
        # Agent 2: Profiler (uses cached profile)
        # Profile is already computed, just reference it
        
        # Agent 3: Tilt Detector (cross-references all data)
        tilt_analysis = self.tilt_detector.detect_tilt(
            market_state,
            user_behavior,
            self.trader_profile
        )
        
        return {
            'regime': regime_analysis,
            'tilt': tilt_analysis,
            'profile': self.trader_profile
        }
    
    def intervene(self, reasoning: Dict) -> Dict:
        """
        INTERVENE: Generate and deliver intervention
        """
        tilt_analysis = reasoning['tilt']
        
        intervention = self.intervention_engine.generate_intervention(
            tilt_analysis,
            self.trader_profile,
            self.current_market_state
        )
        
        # Create UI overlay if needed
        if intervention['type'] != 'NONE':
            ui_overlay = self.intervention_engine.create_ui_overlay(
                intervention,
                historical_reference=f"Similar to your {self.trader_profile.get('dominant_bias')} pattern"
            )
            intervention['ui'] = ui_overlay
        
        return intervention
    
    def run_cognitive_loop(self, ticker: str, trades_df: pd.DataFrame, user_action: str = None) -> Dict:
        """
        Full Perceive-Reason-Intervene cycle
        """
        # Initialize profile if first run
        if not self.trader_profile:
            self.initialize_trader_profile(trades_df)
        
        # PERCEIVE
        perception = self.perceive(ticker, user_action)
        
        # REASON
        reasoning = self.reason(perception)
        
        # INTERVENE
        intervention = self.intervene(reasoning)
        
        return {
            'perception': perception,
            'reasoning': reasoning,
            'intervention': intervention,
            'system_status': 'ACTIVE' if self.system_active else 'PAUSED'
        }
    
    def get_system_diagnostics(self) -> Dict:
        """Returns full system state for debugging"""
        return {
            'trader_profile': self.trader_profile,
            'current_market': self.current_market_state,
            'intervention_stats': self.intervention_engine.get_intervention_stats(),
            'user_interaction_count': len(self.user_stream.interaction_buffer)
        }
