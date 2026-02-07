"""
Antifragile Mirror - Streamlit Interface
Biometric-Behavioral Multi-Agent Trading System
"""
import streamlit as st
import pandas as pd
from antifragile_controller import AntifragileController
import data_manager
import os
import json

st.set_page_config(
    page_title="Antifragile Mirror",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS for intervention overlays
st.markdown("""
<style>
.intervention-critical {
    padding: 20px;
    border-radius: 10px;
    background-color: #ff4444;
    color: white;
    font-weight: bold;
    border: 3px solid #cc0000;
}
.intervention-warning {
    padding: 20px;
    border-radius: 10px;
    background-color: #ff9800;
    color: white;
    border: 2px solid #f57c00;
}
.intervention-nudge {
    padding: 15px;
    border-radius: 10px;
    background-color: #ffeb3b;
    color: #333;
    border: 2px solid #fbc02d;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🧠 Antifragile Mirror")
st.markdown("**Biometric-Behavioral Multi-Agent Trading System**")
st.caption("Perceive → Reason → Intervene")

# Sidebar
st.sidebar.header("⚙️ System Configuration")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    st.sidebar.success("✅ API Connected")
else:
    st.sidebar.error("❌ API Key Required")
    st.stop()

# Initialize session state
if 'controller' not in st.session_state:
    st.session_state.controller = AntifragileController(api_key)
    st.session_state.trades = pd.DataFrame()
    st.session_state.initialized = False

# Load demo data
if st.sidebar.button("🔄 Load Demo Trades"):
    st.session_state.trades = data_manager.generate_mock_trades(30)
    st.sidebar.success("Demo data loaded!")

# Main Interface
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Trading Dashboard")
    
    if st.session_state.trades.empty:
        st.info("Load demo trades from sidebar to begin")
    else:
        # Display trades
        st.dataframe(st.session_state.trades.tail(10), use_container_width=True)
        
        # Metrics
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric("Total Trades", len(st.session_state.trades))
        with metric_col2:
            win_rate = len(st.session_state.trades[st.session_state.trades['PnL'] > 0]) / len(st.session_state.trades) * 100
            st.metric("Win Rate", f"{win_rate:.1f}%")
        with metric_col3:
            total_pnl = st.session_state.trades['PnL'].sum()
            st.metric("Total P&L", f"${total_pnl:.2f}")

with col2:
    st.header("🎯 System Status")
    
    if not st.session_state.initialized and not st.session_state.trades.empty:
        if st.button("🚀 Initialize System", type="primary"):
            with st.spinner("Profiling trader..."):
                profile = st.session_state.controller.initialize_trader_profile(st.session_state.trades)
                st.session_state.initialized = True
                st.success("System initialized!")
                st.json(profile)
    
    if st.session_state.initialized:
        st.success("✅ System Active")
        
        # Display trader profile
        with st.expander("👤 Trader Profile"):
            st.json(st.session_state.controller.trader_profile)

# Cognitive Loop Simulator
st.markdown("---")
st.header("🔄 Cognitive Loop Simulator")

sim_col1, sim_col2, sim_col3 = st.columns(3)

with sim_col1:
    ticker = st.selectbox("Select Ticker", ['AAPL', 'TSLA', 'NVDA', 'BTC-USD', 'SPY'])

with sim_col2:
    user_action = st.selectbox("Simulate User Action", [
        'None',
        'place_order',
        'cancel_order',
        'modify_order',
        'check_position'
    ])

with sim_col3:
    st.write("")
    st.write("")
    run_loop = st.button("▶️ Run Cognitive Loop", type="primary")

if run_loop and st.session_state.initialized:
    with st.spinner("Running Perceive-Reason-Intervene cycle..."):
        # Simulate multiple rapid actions for tilt detection
        if user_action != 'None':
            for _ in range(3):  # Simulate rapid-fire behavior
                st.session_state.controller.user_stream.capture_interaction(user_action)
        
        result = st.session_state.controller.run_cognitive_loop(
            ticker,
            st.session_state.trades,
            user_action if user_action != 'None' else None
        )
        
        # Display results
        st.markdown("### 📡 Perception Layer")
        perc_col1, perc_col2 = st.columns(2)
        
        with perc_col1:
            st.markdown("**Market State**")
            st.json(result['perception']['market'])
        
        with perc_col2:
            st.markdown("**User Behavior**")
            st.json(result['perception']['user'])
        
        st.markdown("### 🧠 Cognitive Layer")
        cog_col1, cog_col2 = st.columns(2)
        
        with cog_col1:
            st.markdown("**Regime Analysis**")
            st.write(result['reasoning']['regime'].get('analysis', 'N/A'))
        
        with cog_col2:
            st.markdown("**Tilt Detection**")
            tilt = result['reasoning']['tilt']
            st.metric("Tilt Score", f"{tilt.get('tilt_score', 0)}/10")
            if tilt.get('llm_analysis'):
                st.info(tilt['llm_analysis'])
        
        st.markdown("### 🎯 Action Layer")
        intervention = result['intervention']
        
        if intervention['type'] == 'HARD_LOCK':
            st.markdown(f"""
            <div class="intervention-critical">
                <h2>🚨 {intervention.get('ui', {}).get('title', 'HARD LOCK')}</h2>
                <p>{intervention['message']}</p>
                <p><strong>Action:</strong> Trading locked for 5 minutes</p>
            </div>
            """, unsafe_allow_html=True)
        
        elif intervention['type'] == 'CRITICAL':
            st.markdown(f"""
            <div class="intervention-warning">
                <h3>⚠️ {intervention.get('ui', {}).get('title', 'WARNING')}</h3>
                <p>{intervention['message']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        elif intervention['type'] == 'SOFT_NUDGE':
            st.markdown(f"""
            <div class="intervention-nudge">
                <h4>💡 {intervention.get('ui', {}).get('title', 'Notice')}</h4>
                <p>{intervention['message']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            st.success("✅ No intervention needed - trader state is healthy")

# System Diagnostics
with st.expander("🔧 System Diagnostics"):
    if st.session_state.initialized:
        diagnostics = st.session_state.controller.get_system_diagnostics()
        st.json(diagnostics)

# Footer
st.markdown("---")
st.caption("Built with Gemini 2.0 Flash | Antifragile Mirror v1.0")
