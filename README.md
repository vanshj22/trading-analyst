# 🧠 Antifragile Mirror - Trading Psychology AI

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.23+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A Biometric-Behavioral Multi-Agent System that detects emotional trading and intervenes before you blow up your account.**

Unlike traditional trading bots that focus on price action, the Antifragile Mirror monitors the **delta between market state and your mental state** to prevent emotional trading decisions.

---

## 🎯 What It Does

- **Profiles Your Psychology**: Analyzes your trading history to identify biases (Loss Aversion, FOMO, Revenge Trading)
- **Detects Tilt in Real-Time**: Uses 3 AI agents to detect when you're about to make emotional decisions
- **Intervenes Automatically**: Provides warnings or temporarily locks trading when panic is detected

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get API Key
Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com)

### 3. Set Environment Variable
```bash
# Windows
set GEMINI_API_KEY=your_key_here

# Mac/Linux
export GEMINI_API_KEY=your_key_here
```

### 4. Run the App
```bash
streamlit run antifragile_app.py
```

Open `http://localhost:8501` in your browser.

---

## 📖 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get running in 5 minutes
- **[App Navigation Guide](APP_NAVIGATION_GUIDE.md)** - How to use the interface
- **[Architecture](ARCHITECTURE.md)** - System design and components
- **[Full Documentation](ANTIFRAGILE_README.md)** - Complete technical docs

---

## 🏗️ Architecture

```
PERCEIVE (Market + User Behavior)
    ↓
REASON (3 AI Agents: Market Analyst, Profiler, Tilt Detector)
    ↓
INTERVENE (Soft Nudge / Critical Warning / Hard Lock)
```

### The 3 AI Agents

1. **Market Analyst**: Detects regime shifts (LOW_VOL → HIGH_VOL → CRISIS)
2. **Profiler**: Identifies your psychological biases from trade history
3. **Tilt Detector**: Cross-references market chaos + your behavior + your history

---

## 🎨 Features

### ✅ Perception Layer
- Real-time market regime detection
- User interaction velocity tracking
- Order pattern analysis

### ✅ Cognitive Layer
- Multi-agent reasoning system
- 5 bias types detected:
  - Loss Aversion / Revenge Trading
  - FOMO Overtrading
  - Poor Edge Execution
  - Cutting Winners Early
  - Disciplined Trader

### ✅ Action Layer
- **Soft Nudge** (Score 5-6): Gentle behavioral notifications
- **Critical Warning** (Score 7-8): Non-dismissible alerts
- **Hard Lock** (Score 9-10): Temporary trading suspension

---

## 📊 Example: Detecting "The Tilt"

**Scenario:** You lose $500 on TSLA, then immediately try to "win it back" with 3x position size.

**System Response:**
```
PERCEIVE:
- Market: HIGH_VOL regime, TSLA volatility = 0.03
- User: 5 actions in 2 minutes, 3 order cancels

REASON:
- Market Analyst: "HIGH_VOL regime detected"
- Profiler: "User has 5 revenge trading patterns"
- Tilt Detector: "Tilt Score 9/10 → HARD LOCK"

INTERVENE:
🚨 RECOVERY MODE DETECTED
"You are attempting to 'win back' a loss. This is a cognitive 
error, not a trading signal. Trading suspended for 5 minutes."
```

---

## 🧪 Testing

Run the test suite:
```bash
python test_antifragile.py
```

Run usage examples:
```bash
python examples.py
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM Reasoning | Gemini 2.0 Flash |
| Orchestration | Custom Python |
| Market Data | yfinance |
| UI | Streamlit |
| Memory | In-memory (Pinecone-ready) |

---

## 📁 Project Structure

```
trading-analyst/
├── perception_layer.py          # Market & user stream processing
├── cognitive_layer.py           # 3 AI agents
├── action_layer.py              # Intervention engine
├── antifragile_controller.py    # Orchestration
├── antifragile_app.py           # Streamlit UI
├── config.py                    # Configuration
├── test_antifragile.py          # Testing
├── data_manager.py              # Trade data generator
└── requirements.txt             # Dependencies
```

---

## 🎯 Use Cases

### For Individual Traders
- Prevent revenge trading after losses
- Detect FOMO entries during pumps
- Identify when you're overtrading

### For Trading Firms
- Monitor trader psychology across teams
- Detect risk-taking behavior patterns
- Implement automated risk controls

### For Trading Educators
- Teach students about trading psychology
- Demonstrate emotional trading patterns
- Provide objective feedback

---

## 🔮 Roadmap

### Phase 2 (Ready for Integration)
- [ ] Pinecone Vector DB for long-term memory
- [ ] Apple Watch heart rate monitoring
- [ ] Interactive Brokers API integration
- [ ] Apache Flink real-time streaming
- [ ] Phi-4 SLM for low-latency monitoring

---

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines first.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

Built with:
- [Gemini 2.0 Flash](https://ai.google.dev/) - LLM reasoning
- [Streamlit](https://streamlit.io) - UI framework
- [yfinance](https://github.com/ranaroussi/yfinance) - Market data

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**⚠️ Disclaimer:** This is an educational tool. Not financial advice. Trade at your own risk.

---

*"The best trade is the one you don't make when you're tilted."* 🧠
