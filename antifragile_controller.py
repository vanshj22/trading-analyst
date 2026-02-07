"""
Orchestration Layer: Lead Controller
Coordinates the Perceive-Reason-Intervene loop across all agents
Enhanced with Market Intelligence and Social Content capabilities
"""
from perception_layer import MarketStreamProcessor, UserStreamProcessor
from cognitive_layer import MarketAnalystAgent, ProfilerAgent, TiltDetectorAgent
from action_layer import InterventionEngine
from market_intelligence import MarketIntelligence
from persona_bot import PersonaBot
from typing import Dict, List
import pandas as pd

class AntifragileController:
    """
    Lead Controller for the Antifragile Mirror System
    Orchestrates the cognitive loop: Perceive → Reason → Intervene
    Now includes Market Intelligence and Social Content generation
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
        
        # NEW: Market Intelligence Layer
        self.market_intelligence = MarketIntelligence(api_key)
        
        # NEW: Social Content Layer
        self.persona_bot = PersonaBot(api_key)
        
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
    
    # ===== NEW: Market Intelligence Methods =====
    
    def explain_market_move(self, ticker: str) -> Dict:
        """
        Generates a comprehensive "Why it moved" explanation for a ticker.
        Combines news, technicals, and LLM analysis.
        """
        return self.market_intelligence.explain_market_move(ticker)
    
    def get_market_technicals(self, ticker: str) -> Dict:
        """Returns technical indicators for a ticker."""
        return self.market_intelligence.calculate_technicals(ticker)
    
    def get_market_news(self, ticker: str) -> List[Dict]:
        """Returns recent news for a ticker."""
        return self.market_intelligence.fetch_news(ticker)
    
    def get_market_sentiment(self, ticker: str) -> Dict:
        """Returns sentiment analysis for a ticker."""
        return self.market_intelligence.get_market_sentiment(ticker)
    
    def generate_daily_briefing(self, tickers: List[str]) -> str:
        """Generates a morning market briefing for multiple tickers."""
        return self.market_intelligence.generate_daily_briefing(tickers)
    
    # ===== NEW: Social Content Methods =====
    
    def get_available_personas(self) -> List[str]:
        """Returns list of available AI personas for content generation."""
        return self.persona_bot.get_available_personas()
    
    def generate_social_content(self, ticker: str, persona_name: str, platform: str = "twitter") -> str:
        """
        Generates social media content for a ticker using specified persona.
        
        Args:
            ticker: Stock ticker symbol
            persona_name: Name of the AI persona to use
            platform: 'twitter', 'thread', or 'linkedin'
        """
        # Get market data for context
        technicals = self.market_intelligence.calculate_technicals(ticker)
        news = self.market_intelligence.fetch_news(ticker, max_items=3)
        
        if platform == "twitter":
            return self.persona_bot.generate_market_update(persona_name, ticker, technicals, news)
        elif platform == "thread":
            context = self._build_market_context(ticker, technicals, news)
            return self.persona_bot.generate_twitter_thread(persona_name, f"{ticker} analysis", context)
        elif platform == "linkedin":
            context = self._build_market_context(ticker, technicals, news)
            return self.persona_bot.generate_linkedin_post(persona_name, f"{ticker} market analysis", context)
        else:
            return self.persona_bot.generate_market_update(persona_name, ticker, technicals, news)
    
    def generate_briefing_social(self, tickers: List[str], persona_name: str) -> Dict:
        """
        Generates social media versions of a daily briefing.
        Returns both Twitter thread and LinkedIn post.
        """
        briefing = self.generate_daily_briefing(tickers)
        return self.persona_bot.generate_daily_briefing_social(briefing, persona_name)
    
    def _build_market_context(self, ticker: str, technicals: Dict, news: List[Dict]) -> str:
        """Helper to build market context string for content generation."""
        parts = [f"Ticker: {ticker}"]
        
        if technicals and 'error' not in technicals:
            parts.append(
                f"Price: ${technicals.get('current_price', 'N/A')} "
                f"({technicals.get('price_change_1d', 0):+.2f}% today)"
            )
            parts.append(f"RSI: {technicals.get('rsi', 'N/A')} ({technicals.get('rsi_signal', '')})")
            parts.append(f"Trend: {technicals.get('trend', 'N/A')}")
        
        if news:
            parts.append("Recent News: " + " | ".join([n['title'] for n in news[:3]]))
        
        return " | ".join(parts)
    
    # ===== NEW: Combined Analyst + Behavioral Loop =====
    
    def run_full_analyst_loop(self, ticker: str, trades_df: pd.DataFrame = None, 
                               user_action: str = None) -> Dict:
        """
        Runs both the behavioral cognitive loop AND market intelligence.
        This is the "magic" combination the hackathon is looking for.
        """
        result = {
            'ticker': ticker,
            'market_explanation': None,
            'behavioral_analysis': None,
            'combined_insight': None
        }
        
        # Get market explanation
        result['market_explanation'] = self.explain_market_move(ticker)
        
        # Run behavioral loop if trade data provided
        if trades_df is not None and not trades_df.empty:
            result['behavioral_analysis'] = self.run_cognitive_loop(ticker, trades_df, user_action)
            
            # Generate combined insight if both are available and no errors
            market_exp = result['market_explanation']
            has_valid_market = (market_exp and 
                                'error' not in market_exp and 
                                market_exp.get('explanation') is not None)
            
            if has_valid_market and result['behavioral_analysis']:
                result['combined_insight'] = self._generate_combined_insight(
                    result['market_explanation'],
                    result['behavioral_analysis']
                )
            elif not has_valid_market:
                result['combined_insight'] = "Market data unavailable. Focus on your trading discipline."
        
        return result
    
    def _generate_combined_insight(self, market_exp: Dict, behavioral: Dict) -> str:
        """
        Generates the "killer feature" insight that combines market and behavior.
        E.g., "The market just did X, and based on your history, you tend to Y in these situations"
        """
        import google.generativeai as genai
        
        # Safe extraction with defaults
        technicals = market_exp.get('technicals') or {}
        market_regime = technicals.get('trend', 'UNKNOWN') if technicals else 'UNKNOWN'
        price_change = technicals.get('price_change_1d', 0) if technicals else 0
        explanation = market_exp.get('explanation') or 'Market data unavailable'
        news_summary = explanation[:200] if explanation else 'N/A'
        
        # Behavioral data
        tilt_score = behavioral.get('reasoning', {}).get('tilt', {}).get('tilt_score', 0)
        dominant_bias = self.trader_profile.get('dominant_bias', 'UNKNOWN')
        
        prompt = f"""You are a trading psychology coach. Generate a combined insight.

MARKET SITUATION:
- Trend: {market_regime}
- Price Change: {price_change:+.2f}%
- News Summary: {news_summary}

TRADER BEHAVIOR:
- Dominant Bias: {dominant_bias}
- Current Tilt Score: {tilt_score}/10
- Historical Pattern: Tends to trade emotionally after losses

Generate ONE personalized sentence that:
1. Acknowledges the market move
2. References their specific behavioral pattern
3. Gives actionable guidance

Example format: "The market just [X], and based on your history, you tend to [Y] in these situations. Consider [Z]."

Keep it under 100 words. Be direct and helpful."""

        try:
            model = genai.GenerativeModel('gemini-2.5-pro')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Market is {market_regime}. Your tilt score is {tilt_score}/10. Stay disciplined."
