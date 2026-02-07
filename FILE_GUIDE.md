# 📁 File Structure & Relationships

## Complete File Map

```
trading-analyst/
│
├── 🚀 ANTIFRAGILE MIRROR SYSTEM (New)
│   ├── perception_layer.py          ← Sensory input (Market + User streams)
│   ├── cognitive_layer.py           ← Multi-agent brain (3 agents)
│   ├── action_layer.py              ← Intervention engine
│   ├── antifragile_controller.py    ← Orchestration (Lead controller)
│   ├── antifragile_app.py           ← Streamlit UI
│   ├── config.py                    ← Configuration
│   └── test_antifragile.py          ← Testing suite
│
├── 📚 DOCUMENTATION (New)
│   ├── ANTIFRAGILE_README.md        ← Complete system docs
│   ├── ARCHITECTURE.md              ← Visual architecture
│   ├── QUICKSTART.md                ← 5-minute setup guide
│   └── IMPLEMENTATION_SUMMARY.md    ← What was built
│
├── 🔧 EXISTING SYSTEM (Original)
│   ├── app.py                       ← Original Streamlit app
│   ├── analyst_core.py              ← Original analyst
│   ├── persona_bot.py               ← Social media bot
│   ├── data_manager.py              ← Trade data generator (USED BY ANTIFRAGILE)
│   └── debug_*.py                   ← Debug utilities
│
└── 📦 DEPENDENCIES
    └── requirements.txt             ← Updated with numpy
```

## How Files Connect

### 🔄 Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER STARTS SYSTEM                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  antifragile_app.py  │  ← Streamlit UI
              │  (User Interface)    │
              └──────────┬───────────┘
                         │
                         │ imports
                         ▼
         ┌───────────────────────────────┐
         │ antifragile_controller.py     │  ← Orchestrator
         │ (Lead Controller)             │
         └───────┬───────────────────────┘
                 │
                 │ imports & coordinates
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│Perception│  │Cognitive│  │ Action  │
│  Layer   │  │  Layer  │  │  Layer  │
└─────────┘  └─────────┘  └─────────┘
    │            │            │
    │            │            │
    └────────────┴────────────┘
                 │
                 │ reads config from
                 ▼
         ┌──────────────┐
         │  config.py   │  ← Settings
         └──────────────┘
```

### 📊 Import Chain

```python
# antifragile_app.py
from antifragile_controller import AntifragileController
import data_manager  # Uses existing file!

# antifragile_controller.py
from perception_layer import MarketStreamProcessor, UserStreamProcessor
from cognitive_layer import MarketAnalystAgent, ProfilerAgent, TiltDetectorAgent
from action_layer import InterventionEngine

# All layers import
import config  # For thresholds and settings
```

### 🧪 Testing Flow

```
test_antifragile.py
    │
    ├─→ Imports antifragile_controller
    ├─→ Imports data_manager (generates mock trades)
    ├─→ Tests all components
    └─→ Outputs results to console
```

## File Purposes

### Core System Files

| File | Purpose | Lines | Key Classes |
|------|---------|-------|-------------|
| `perception_layer.py` | Ingests market + user data | ~100 | MarketStreamProcessor, UserStreamProcessor |
| `cognitive_layer.py` | Multi-agent reasoning | ~150 | MarketAnalystAgent, ProfilerAgent, TiltDetectorAgent |
| `action_layer.py` | Generates interventions | ~120 | InterventionEngine |
| `antifragile_controller.py` | Orchestrates everything | ~130 | AntifragileController |
| `antifragile_app.py` | User interface | ~180 | (Streamlit app) |
| `config.py` | Configuration | ~200 | (Settings only) |
| `test_antifragile.py` | Testing | ~60 | (Test functions) |

### Documentation Files

| File | Purpose | For Who |
|------|---------|---------|
| `ANTIFRAGILE_README.md` | Complete documentation | Developers |
| `ARCHITECTURE.md` | System architecture | Technical readers |
| `QUICKSTART.md` | Setup guide | End users |
| `IMPLEMENTATION_SUMMARY.md` | What was built | Project managers |

## Running Different Components

### 1. Run Full System (UI)
```bash
streamlit run antifragile_app.py
```
**Uses:** All 7 core files + data_manager.py

### 2. Run Tests
```bash
python test_antifragile.py
```
**Uses:** All core files except antifragile_app.py

### 3. Use Programmatically
```python
from antifragile_controller import AntifragileController
controller = AntifragileController(api_key)
```
**Uses:** Controller + all layers + config

### 4. Run Original System (Separate)
```bash
streamlit run app.py
```
**Uses:** app.py, analyst_core.py, persona_bot.py, data_manager.py

## Dependency Graph

```
antifragile_app.py
    └── antifragile_controller.py
            ├── perception_layer.py
            │       └── yfinance, numpy, datetime
            ├── cognitive_layer.py
            │       └── google.generativeai, numpy
            ├── action_layer.py
            │       └── google.generativeai, datetime
            └── config.py
                    └── (no dependencies)

data_manager.py (shared with original system)
    └── pandas, numpy, yfinance, datetime
```

## Configuration Hierarchy

```
config.py (Default settings)
    ↓
antifragile_controller.py (Reads config)
    ↓
All agents use config values
    ↓
Can be overridden at runtime
```

## Memory & State Flow

```
1. INITIALIZATION
   trades_df → ProfilerAgent → trader_profile (stored in controller)

2. RUNTIME
   ticker → MarketStreamProcessor → market_state (stored in controller)
   user_action → UserStreamProcessor → interaction_buffer (stored in processor)

3. COGNITIVE LOOP
   market_state + interaction_buffer + trader_profile
       ↓
   Multi-agent reasoning
       ↓
   Intervention (stored in intervention_engine.history)
```

## Which File to Edit For...

| Task | Edit This File |
|------|---------------|
| Change tilt thresholds | `config.py` |
| Add new bias type | `cognitive_layer.py` → ProfilerAgent |
| Modify intervention messages | `action_layer.py` → InterventionEngine |
| Add new market indicator | `perception_layer.py` → MarketStreamProcessor |
| Change UI layout | `antifragile_app.py` |
| Adjust agent coordination | `antifragile_controller.py` |
| Add new test case | `test_antifragile.py` |

## Integration Points (Future)

### For Pinecone Vector DB:
Edit: `cognitive_layer.py` → ProfilerAgent
Add: `vector_store.py` (new file)

### For Apple Watch:
Edit: `perception_layer.py` → UserStreamProcessor
Add: `biometric_stream.py` (new file)

### For Interactive Brokers:
Edit: `antifragile_controller.py`
Add: `broker_integration.py` (new file)

### For LangGraph:
Edit: `antifragile_controller.py`
Replace: Custom orchestration with LangGraph nodes

## Quick Reference

### Start Here:
1. Read: `QUICKSTART.md`
2. Run: `python test_antifragile.py`
3. Explore: `streamlit run antifragile_app.py`

### Understand Architecture:
1. Read: `ARCHITECTURE.md`
2. Read: `ANTIFRAGILE_README.md`

### Customize:
1. Edit: `config.py`
2. Test: `python test_antifragile.py`

### Extend:
1. Read: `IMPLEMENTATION_SUMMARY.md`
2. Edit: Relevant layer file
3. Update: `test_antifragile.py`

---

**Total New Files:** 11 (7 code + 4 docs)
**Total Lines of Code:** ~1,000
**External Dependencies:** 3 (streamlit, google-generativeai, yfinance)
**Integration Ready:** Pinecone, Apple Watch, IB API, LangGraph
