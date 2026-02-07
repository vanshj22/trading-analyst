"""
Action Layer: Intervention Engine
Delivers psychologically calibrated nudges and hard locks
"""
import google.generativeai as genai
from typing import Dict
from datetime import datetime

from config import PRIMARY_MODEL

import time
import random

class InterventionEngine:
    """Generates context-aware interventions using Persona Engine"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(PRIMARY_MODEL)
        self.intervention_history = []
    
    def _generate_with_retry(self, prompt, max_retries=3, base_delay=2):
        """Helper to handle rate limits with exponential backoff"""
        for attempt in range(max_retries):
            try:
                return self.model.generate_content(prompt)
            except Exception as e:
                if "429" in str(e) or "Too Many Requests" in str(e):
                    if attempt < max_retries - 1:
                        sleep_time = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
                        print(f"⚠️ Intervention Engine: Rate limit hit. Retrying in {sleep_time:.1f}s...")
                        time.sleep(sleep_time)
                        continue
                if attempt == max_retries - 1:
                    raise e
                raise e

    def generate_intervention(self, tilt_analysis: Dict, trader_profile: Dict, market_state: Dict) -> Dict:
        """Creates calibrated intervention message"""
        
        severity = self._assess_severity(tilt_analysis)
        
        if severity == "NONE":
            return {'type': 'NONE', 'message': None}
        
        # Build context for LLM
        prompt = f"""You are a trading psychology coach. Generate an intervention message.

SITUATION:
- Tilt Score: {tilt_analysis.get('tilt_score', 0)}/10
- Market Regime: {market_state.get('regime')}
- Trader Profile: Win Rate {trader_profile.get('win_rate')}%, {trader_profile.get('revenge_signals')} revenge patterns
- LLM Analysis: {tilt_analysis.get('llm_analysis', 'N/A')}

INTERVENTION TYPE: {severity}

Generate a message that:
1. Acknowledges the emotional state
2. References their specific pattern
3. Provides actionable guidance
4. Uses firm but supportive tone

Keep it under 100 words. Be direct."""

        try:
            response = self._generate_with_retry(prompt)
            intervention = {
                'type': severity,
                'message': response.text,
                'timestamp': datetime.now().isoformat(),
                'requires_ui_lock': severity in ['HARD_LOCK', 'CRITICAL']
            }
            
            self.intervention_history.append(intervention)
            return intervention
            
        except Exception as e:
            return {'type': 'ERROR', 'message': f'Failed to generate intervention: {str(e)}'}
    
    def _assess_severity(self, tilt_analysis: Dict) -> str:
        """Maps tilt score to intervention type"""
        score = tilt_analysis.get('tilt_score', 0)
        
        # Trigger interventions based on tilt score
        if score >= 9:
            return "HARD_LOCK"
        elif score >= 7:
            return "CRITICAL"
        elif score >= 5:
            return "SOFT_NUDGE"
        else:
            return "NONE"
    
    def create_ui_overlay(self, intervention: Dict, historical_reference: str = None) -> Dict:
        """Formats intervention for UI display"""
        
        if intervention['type'] == 'HARD_LOCK':
            return {
                'title': '🚨 RECOVERY MODE DETECTED',
                'message': intervention['message'],
                'action': 'LOCK_TRADING',
                'duration_minutes': 5,
                'color': 'red',
                'historical_ref': historical_reference or 'Previous blowup pattern detected'
            }
        
        elif intervention['type'] == 'CRITICAL':
            return {
                'title': '⚠️ TILT WARNING',
                'message': intervention['message'],
                'action': 'SHOW_WARNING',
                'color': 'orange',
                'dismissible': False
            }
        
        elif intervention['type'] == 'SOFT_NUDGE':
            return {
                'title': '💡 Behavioral Notice',
                'message': intervention['message'],
                'action': 'SHOW_NOTIFICATION',
                'color': 'yellow',
                'dismissible': True
            }
        
        return {'title': 'System OK', 'message': 'No intervention needed', 'action': 'NONE'}
    
    def get_intervention_stats(self) -> Dict:
        """Returns intervention history analytics"""
        if not self.intervention_history:
            return {'total': 0}
        
        types = [i['type'] for i in self.intervention_history]
        return {
            'total': len(self.intervention_history),
            'soft_nudges': types.count('SOFT_NUDGE'),
            'critical_warnings': types.count('CRITICAL'),
            'hard_locks': types.count('HARD_LOCK'),
            'last_intervention': self.intervention_history[-1]['timestamp']
        }
