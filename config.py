"""
Configuration file for Antifragile Mirror System
Customize thresholds, models, and intervention parameters
"""

# ============================================================================
# LLM CONFIGURATION
# ============================================================================

# Primary reasoning model (options: gemini-2.0-flash-exp, gemini-1.5-pro)
PRIMARY_MODEL = "gemini-1.5-flash"

# Fallback model if primary fails
FALLBACK_MODEL = "gemini-1.5-flash"

# Temperature for LLM responses (0.0 = deterministic, 1.0 = creative)
LLM_TEMPERATURE = 0.3

# ============================================================================
# PERCEPTION LAYER SETTINGS
# ============================================================================

# Market volatility threshold for regime detection (2% = 0.02)
VOLATILITY_THRESHOLD = 0.02

# Volume spike multiplier (1.5 = 50% above average)
VOLUME_SPIKE_MULTIPLIER = 1.5

# User interaction window for velocity analysis (minutes)
INTERACTION_WINDOW_MINUTES = 5

# Maximum interaction buffer size
MAX_INTERACTION_BUFFER = 100

# ============================================================================
# COGNITIVE LAYER SETTINGS
# ============================================================================

# Tilt detection thresholds
TILT_THRESHOLDS = {
    'SOFT_NUDGE': 5,      # Score 5-6
    'CRITICAL': 7,        # Score 7-8
    'HARD_LOCK': 9        # Score 9-10
}

# Panic threshold for volatility (2.5% = 0.025)
PANIC_THRESHOLD = 0.025

# Minimum trades required for profiling
MIN_TRADES_FOR_PROFILE = 10

# Revenge trading detection: consecutive losses threshold
REVENGE_LOSS_THRESHOLD = 2

# FOMO detection: keyword matching
FOMO_KEYWORDS = ['FOMO', 'Revenge', 'rushed', 'panic', 'fear']

# Risk/Reward ratio threshold for "cutting winners early" bias
MIN_RISK_REWARD_RATIO = 1.5

# Win rate threshold for "poor edge" detection (%)
MIN_WIN_RATE = 40

# ============================================================================
# ACTION LAYER SETTINGS
# ============================================================================

# Intervention cooldown duration (minutes)
HARD_LOCK_DURATION = 5
CRITICAL_WARNING_COOLDOWN = 2

# Maximum interventions per hour (prevent spam)
MAX_INTERVENTIONS_PER_HOUR = 10

# Intervention message max length (words)
MAX_INTERVENTION_WORDS = 100

# UI overlay colors
INTERVENTION_COLORS = {
    'HARD_LOCK': '#ff4444',      # Red
    'CRITICAL': '#ff9800',       # Orange
    'SOFT_NUDGE': '#ffeb3b',     # Yellow
    'SUCCESS': '#4caf50'         # Green
}

# ============================================================================
# BEHAVIORAL BIAS DEFINITIONS
# ============================================================================

BIAS_DEFINITIONS = {
    'LOSS_AVERSION_REVENGE': {
        'description': 'Attempts to recover losses immediately',
        'risk_level': 'HIGH',
        'intervention_priority': 9
    },
    'FOMO_OVERTRADING': {
        'description': 'Enters trades based on fear of missing out',
        'risk_level': 'MEDIUM',
        'intervention_priority': 6
    },
    'POOR_EDGE_EXECUTION': {
        'description': 'Low win rate indicates strategy issues',
        'risk_level': 'MEDIUM',
        'intervention_priority': 5
    },
    'CUTTING_WINNERS_EARLY': {
        'description': 'Exits profitable trades too quickly',
        'risk_level': 'LOW',
        'intervention_priority': 4
    },
    'DISCIPLINED_TRADER': {
        'description': 'Follows plan consistently',
        'risk_level': 'LOW',
        'intervention_priority': 0
    }
}

# ============================================================================
# MARKET REGIME DEFINITIONS
# ============================================================================

REGIME_DEFINITIONS = {
    'LOW_VOL': {
        'volatility_max': 0.02,
        'risk_multiplier': 1.0,
        'description': 'Normal market conditions'
    },
    'HIGH_VOL': {
        'volatility_min': 0.02,
        'volatility_max': 0.05,
        'risk_multiplier': 1.5,
        'description': 'Elevated volatility - caution advised'
    },
    'CRISIS': {
        'volatility_min': 0.05,
        'risk_multiplier': 2.5,
        'description': 'Extreme volatility - high risk'
    }
}

# ============================================================================
# SYSTEM BEHAVIOR
# ============================================================================

# Enable/disable features
ENABLE_HARD_LOCK = True          # Allow system to lock trading
ENABLE_BIOMETRIC_INTEGRATION = False  # Apple Watch, etc. (future)
ENABLE_BROKER_API = False        # Direct broker integration (future)

# Logging
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
LOG_INTERVENTIONS = True
LOG_USER_ACTIONS = True

# Performance
CACHE_MARKET_DATA_SECONDS = 60   # Cache market data for 1 minute
PROFILE_UPDATE_FREQUENCY = 100   # Re-profile every N trades

# ============================================================================
# ADVANCED: AGENT WEIGHTS
# ============================================================================

# Weight each agent's contribution to tilt score
AGENT_WEIGHTS = {
    'market_analyst': 0.3,    # 30% weight
    'profiler': 0.4,          # 40% weight
    'user_behavior': 0.3      # 30% weight
}

# ============================================================================
# PROMPTS (Advanced Customization)
# ============================================================================

SYSTEM_PROMPTS = {
    'market_analyst': """You are a market regime analyst. Analyze market conditions 
and classify risk levels. Be concise and data-driven.""",
    
    'tilt_detector': """You are a trading psychology expert. Detect emotional 
trading patterns using chain-of-thought reasoning. Be direct and specific.""",
    
    'intervention_engine': """You are a trading psychology coach. Generate 
supportive but firm interventions. Reference specific patterns and provide 
actionable guidance."""
}

# ============================================================================
# LINKEDIN CONFIGURATION
# ============================================================================

# Default redirect URI for local development
LINKEDIN_REDIRECT_URI = "http://localhost:8501"

# Scopes required for posting and user profile
LINKEDIN_SCOPES = ["w_member_social", "openid", "profile", "email"]

# ============================================================================
# EXPORT
# ============================================================================

def get_config():
    """Returns all configuration as a dictionary"""
    return {
        'llm': {
            'primary_model': PRIMARY_MODEL,
            'fallback_model': FALLBACK_MODEL,
            'temperature': LLM_TEMPERATURE
        },
        'perception': {
            'volatility_threshold': VOLATILITY_THRESHOLD,
            'volume_spike_multiplier': VOLUME_SPIKE_MULTIPLIER,
            'interaction_window': INTERACTION_WINDOW_MINUTES
        },
        'cognitive': {
            'tilt_thresholds': TILT_THRESHOLDS,
            'panic_threshold': PANIC_THRESHOLD,
            'min_trades': MIN_TRADES_FOR_PROFILE
        },
        'action': {
            'hard_lock_duration': HARD_LOCK_DURATION,
            'max_interventions_per_hour': MAX_INTERVENTIONS_PER_HOUR
        },
        'features': {
            'enable_hard_lock': ENABLE_HARD_LOCK,
            'enable_biometrics': ENABLE_BIOMETRIC_INTEGRATION,
            'enable_broker_api': ENABLE_BROKER_API
        }
    }

if __name__ == "__main__":
    import json
    print(json.dumps(get_config(), indent=2))
