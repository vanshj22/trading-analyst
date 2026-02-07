# 🚀 Quick Start Guide - Antifragile Mirror

## What is This?

The Antifragile Mirror is a **trading psychology AI** that detects when you're about to make emotional trading decisions and intervenes before you blow up your account.

It doesn't trade for you. It **protects you from yourself**.

## Installation (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Gemini API Key
1. Go to https://aistudio.google.com
2. Create a free API key
3. Set it in your environment:

**Windows:**
```cmd
set GEMINI_API_KEY=your_key_here
```

**Mac/Linux:**
```bash
export GEMINI_API_KEY=your_key_here
```

### 3. Run the System
```bash
streamlit run antifragile_app.py
```

## First Time Setup

### Step 1: Load Your Trade History
- Click "🔄 Load Demo Trades" in the sidebar
- Or upload your own CSV (format: Date, Ticker, Side, Entry Price, Exit Price, Size, PnL)

### Step 2: Initialize System
- Click "🚀 Initialize System"
- The AI will analyze your trading patterns
- You'll see your psychological profile:
  - Win rate
  - Revenge trading signals
  - Dominant bias (FOMO, Loss Aversion, etc.)

### Step 3: Run Cognitive Loop
- Select a ticker (e.g., BTC-USD)
- Simulate a user action (e.g., "place_order")
- Click "▶️ Run Cognitive Loop"

The system will:
1. **Perceive**: Check market conditions + your behavior
2. **Reason**: Analyze if you're in tilt
3. **Intervene**: Show warning if needed

## Understanding Interventions

### 🟢 No Intervention (Score 0-4)
You're trading rationally. System stays silent.

### 🟡 Soft Nudge (Score 5-6)
```
💡 Behavioral Notice
"You've placed 3 orders in 2 minutes. Your history shows 
this pattern precedes losses. Consider taking a breath."
```
→ Dismissible notification

### 🟠 Critical Warning (Score 7-8)
```
⚠️ TILT WARNING
"Market volatility is HIGH and you're increasing position size.
This matches your 'revenge trading' pattern from last month."
```
→ Non-dismissible, requires acknowledgment

### 🔴 Hard Lock (Score 9-10)
```
🚨 RECOVERY MODE DETECTED
"You are attempting to 'win back' a loss. This is a cognitive 
error, not a trading signal. Trading suspended for 5 minutes."
```
→ Trading disabled temporarily

## Testing the System

Run the test script:
```bash
python test_antifragile.py
```

This will:
- ✅ Verify API connection
- ✅ Generate mock trades
- ✅ Profile a trader
- ✅ Simulate normal trading
- ✅ Simulate tilt detection

## Real-World Usage

### Scenario 1: Flash Crash
```
You're trading BTC. Price drops 5% in 10 minutes.
You feel the urge to "buy the dip" with 3x your normal size.

→ System detects:
  - HIGH_VOL regime
  - Position size anomaly
  - Matches your "FOMO" bias

→ Intervention:
  "⚠️ Your position size is 3x normal during high volatility.
   Your history shows 70% loss rate in this scenario."
```

### Scenario 2: Revenge Trading
```
You just lost $500 on TSLA. You immediately open a new 
position to "win it back."

→ System detects:
  - Loss followed by immediate re-entry
  - Matches "revenge trading" pattern
  - Rapid order placement

→ Intervention:
  "🚨 HARD LOCK - You're attempting to recover a loss.
   Trading suspended for 5 minutes."
```

## Customization

### Adjust Tilt Thresholds
Edit `cognitive_layer.py`:
```python
class TiltDetectorAgent:
    def __init__(self, api_key: str):
        self.panic_threshold = 0.025  # Increase for less sensitivity
```

### Change Intervention Duration
Edit `action_layer.py`:
```python
'duration_minutes': 10,  # Change from 5 to 10 minutes
```

### Add Custom Biases
Edit `cognitive_layer.py` → `ProfilerAgent.detect_bias_type()`:
```python
elif profile['avg_hold_time'] < 5:  # minutes
    return "SCALPING_ADDICTION"
```

## Next Steps

1. **Connect Real Broker**: Integrate with Interactive Brokers API
2. **Add Biometrics**: Connect Apple Watch for heart rate monitoring
3. **Deploy Production**: Use Apache Flink for real-time streaming

## Troubleshooting

### "API Key not found"
```bash
# Check if set
echo $GEMINI_API_KEY  # Mac/Linux
echo %GEMINI_API_KEY%  # Windows

# Set it again
export GEMINI_API_KEY=your_key
```

### "No module named 'perception_layer'"
```bash
# Make sure you're in the right directory
cd trading-analyst
python test_antifragile.py
```

### "Tilt never detected"
The system is conservative by default. To test:
1. Simulate 10+ rapid actions
2. Use a high-volatility ticker (BTC-USD)
3. Check that your trade history has loss patterns

## Support

- 📖 Full docs: `ANTIFRAGILE_README.md`
- 🏗️ Architecture: `ARCHITECTURE.md`
- 🧪 Test script: `test_antifragile.py`

## Philosophy

> "The best trade is the one you don't make when you're tilted."

This system doesn't make you a better trader. It prevents you from being your worst enemy.

---

Built for 2026 agentic AI standards 🚀
