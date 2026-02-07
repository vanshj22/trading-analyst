# 🧠 Antifragile Mirror - Biometric-Behavioral Multi-Agent System

## Overview
The **Antifragile Mirror** is a next-generation trading psychology system that monitors the **delta between market state and trader mental state**. Unlike traditional trading bots focused on price action, this system detects and intervenes when a trader's emotional state creates risk.

## Architecture: The Cognitive Loop

```
┌─────────────────────────────────────────────────────────┐
│                   PERCEIVE-REASON-INTERVENE             │
└─────────────────────────────────────────────────────────┘

1. PERCEPTION LAYER (Sensory Input)
   ├── Market Stream: Price, volatility, regime shifts
   └── User Stream: Interaction velocity, order patterns

2. COGNITIVE LAYER (Multi-Agent Brain)
   ├── Market Analyst: Detects regime changes
   ├── Profiler: Identifies latent biases (loss aversion, FOMO)
   └── Tilt Detector: Cross-references market vs. mental state

3. ACTION LAYER (Intervention)
   ├── Soft Nudge: Behavioral notifications
   ├── Critical Warning: High-priority alerts
   └── Hard Lock: Temporary trading suspension
```

## System Components

### 1. Perception Layer (`perception_layer.py`)
**Purpose:** Dual-stream data ingestion

- **MarketStreamProcessor**: Captures real-time market conditions
  - Volatility calculation
  - Regime detection (LOW_VOL → HIGH_VOL transitions)
  - Volume spike detection

- **UserStreamProcessor**: Tracks behavioral patterns
  - Interaction velocity (rapid-fire orders = panic)
  - Cancel/replace patterns
  - Recent P&L sequence analysis

### 2. Cognitive Layer (`cognitive_layer.py`)
**Purpose:** Multi-agent reasoning system

#### Agent 1: Market Analyst
- Identifies regime shifts using LLM reasoning
- Classifies risk levels (LOW → EXTREME)
- Provides context-aware trader advice

#### Agent 2: Profiler
- Vectorizes 1,000+ trades to detect biases
- Identifies patterns:
  - Loss Aversion / Revenge Trading
  - FOMO Overtrading
  - Cutting Winners Early
- Calculates risk/reward ratios

#### Agent 3: Tilt Detector
- **Chain-of-Thought reasoning** to detect emotional trading
- Cross-references:
  - Market volatility
  - User interaction velocity
  - Historical bias patterns
- Outputs tilt score (0-10) and intervention requirement

### 3. Action Layer (`action_layer.py`)
**Purpose:** Psychologically calibrated interventions

#### Intervention Types:
1. **SOFT_NUDGE** (Score 5-6)
   - "Notice your heart rate is up and BTC just dipped..."
   - Dismissible notification

2. **CRITICAL** (Score 7-8)
   - "RECOVERY MODE DETECTED - matches your Aug 2025 blowup pattern"
   - Non-dismissible warning

3. **HARD_LOCK** (Score 9-10)
   - Temporarily disables trading (5-minute cooldown)
   - Requires explicit override

### 4. Orchestration (`antifragile_controller.py`)
**Purpose:** Lead controller coordinating all agents

```python
# Full cognitive loop
result = controller.run_cognitive_loop(
    ticker='BTC-USD',
    trades_df=historical_trades,
    user_action='place_order'
)
```

**Flow:**
1. Initialize trader profile (one-time)
2. Perceive: Capture market + user state
3. Reason: Run all 3 agents in parallel
4. Intervene: Generate calibrated response

## Tech Stack (2026 Standards)

| Component | Technology |
|-----------|-----------|
| LLM Reasoning | Gemini 2.0 Flash (can swap to DeepSeek-V3/Claude 3.5) |
| Orchestration | Custom Python (LangGraph-ready) |
| Memory | In-memory (Pinecone/Zep integration ready) |
| Market Data | yfinance (Apache Flink for production) |
| UI | Streamlit |

## Installation

```bash
# Clone and navigate
cd trading-analyst

# Install dependencies
pip install -r requirements.txt

# Set API key
export GEMINI_API_KEY="your_key_here"

# Run the system
streamlit run antifragile_app.py
```

## Usage

### 1. Initialize System
```python
from antifragile_controller import AntifragileController
import pandas as pd

# Load your trade history
trades_df = pd.read_csv('my_trades.csv')

# Initialize controller
controller = AntifragileController(api_key='your_key')

# Profile trader (one-time)
profile = controller.initialize_trader_profile(trades_df)
print(f"Dominant bias: {profile['dominant_bias']}")
```

### 2. Run Cognitive Loop
```python
# Simulate live trading scenario
result = controller.run_cognitive_loop(
    ticker='TSLA',
    trades_df=trades_df,
    user_action='cancel_order'  # Simulates user canceling order
)

# Check intervention
if result['intervention']['type'] == 'HARD_LOCK':
    print("🚨 TRADING LOCKED - Tilt detected!")
```

### 3. Monitor System
```python
# Get diagnostics
diagnostics = controller.get_system_diagnostics()
print(f"Interventions today: {diagnostics['intervention_stats']['total']}")
```

## Example: Detecting "The Tilt"

**Scenario:** Trader loses 2% in 10 minutes, then doubles position size

```
PERCEPTION:
- Market: HIGH_VOL regime, BTC flash crash
- User: 8 actions in 5 minutes, 4 order cancels

REASONING:
- Market Analyst: "CRISIS regime detected"
- Profiler: "Trader has 5 revenge trading patterns"
- Tilt Detector: "Tilt Score 9/10 - CRITICAL"

INTERVENTION:
🚨 HARD LOCK ACTIVATED
"You are attempting to 'win back' a loss. This matches your 
Aug 2025 blowup pattern. Trading suspended for 5 minutes."
```

## Roadmap

### Phase 1 (Current)
- ✅ Core multi-agent system
- ✅ Tilt detection
- ✅ Basic interventions

### Phase 2 (Next)
- [ ] Biometric integration (Apple Watch heart rate)
- [ ] Vector DB for long-term memory (Pinecone)
- [ ] Real-time streaming (Apache Flink)

### Phase 3 (Future)
- [ ] Local SLM for low-latency monitoring (Phi-4)
- [ ] Broker API integration (Interactive Brokers)
- [ ] Multi-user deployment

## Key Innovations

1. **Behavioral Alpha**: Generates edge from psychology, not price patterns
2. **Predictive Intervention**: Stops blowups before they happen
3. **Personalized**: Learns YOUR specific tilt triggers
4. **Non-Invasive**: Doesn't trade for you, just prevents bad decisions

## License
MIT

## Credits
Built for 2026 agentic AI standards using Gemini 2.0 Flash
