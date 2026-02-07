"""
Action Layer: Intervention Engine
Delivers psychologically calibrated nudges and hard locks
"""
import google.generativeai as genai
from typing import Dict
from datetime import datetime

class InterventionEngine:
    """Generates context-aware interventions using Persona Engine"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        self.intervention_history = []
    
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
            response = self.model.generate_content(prompt)
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
        requires_intervention = tilt_analysis.get('requires_intervention', False)
        
        if not requires_intervention:
            return "NONE"
        elif score >= 9:
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
