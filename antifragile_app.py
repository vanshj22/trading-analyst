"""
Antifragile Mirror - Streamlit Interface
Biometric-Behavioral Multi-Agent Trading System
Enhanced with Market Intelligence and Social Content Studio
"""
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from antifragile_controller import AntifragileController
import data_manager
import os
import json

# Load environment variables from .env file
load_dotenv()

st.set_page_config(
    page_title="Antifragile Mirror",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS for intervention overlays and styling
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
.market-card {
    padding: 15px;
    border-radius: 10px;
    background-color: #1e1e1e;
    border: 1px solid #333;
    margin: 10px 0;
}
.social-preview {
    padding: 15px;
    border-radius: 10px;
    background-color: #0a0a0a;
    border: 1px solid #444;
    font-family: monospace;
    white-space: pre-wrap;
}
.copy-button {
    background-color: #4CAF50;
    color: white;
    padding: 8px 16px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🧠 Antifragile Mirror")
st.markdown("**AI-Powered Trading Analyst + Behavioral Coach + Social Content Engine**")

# Sidebar - Auto-load API key from .env
st.sidebar.header("⚙️ Configuration")

# Get API key from environment (loaded from .env)
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
    st.session_state.last_explanation = None
    st.session_state.last_social_content = None

# Load demo data
if st.sidebar.button("🔄 Load Demo Trades"):
    st.session_state.trades = data_manager.generate_mock_trades(30)
    st.sidebar.success("Demo data loaded!")

# Ticker selection (global)
st.sidebar.markdown("---")
st.sidebar.subheader("📈 Select Ticker")
ticker = st.sidebar.selectbox("Ticker", ['AAPL', 'TSLA', 'NVDA', 'BTC-USD', 'SPY', 'GOOGL', 'AMZN', 'META'])

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Trading Dashboard", "🔍 Market Analyst", "📱 Social Studio", "🧠 Behavioral Coach"])

# ==================== TAB 1: TRADING DASHBOARD ====================
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 Trading Dashboard")
        
        if st.session_state.trades.empty:
            st.info("👈 Load demo trades from sidebar to begin")
        else:
            st.dataframe(st.session_state.trades.tail(10), use_container_width=True)
            
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
            with st.expander("👤 Trader Profile"):
                st.json(st.session_state.controller.trader_profile)

# ==================== TAB 2: MARKET ANALYST ====================
with tab2:
    st.header(f"🔍 Market Analyst: {ticker}")
    st.caption("Real-time market intelligence with AI-powered explanations")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🔎 Analyze Market", type="primary", key="analyze_market"):
            with st.spinner(f"Analyzing {ticker}..."):
                explanation = st.session_state.controller.explain_market_move(ticker)
                st.session_state.last_explanation = explanation
        
        if st.session_state.last_explanation:
            exp = st.session_state.last_explanation
            
            if 'error' in exp:
                st.error(f"Error: {exp['error']}")
            else:
                # Technicals
                tech = exp.get('technicals', {})
                if tech and 'error' not in tech:
                    st.subheader("📈 Technical Overview")
                    tcol1, tcol2, tcol3 = st.columns(3)
                    with tcol1:
                        change = tech.get('price_change_1d', 0)
                        st.metric("Price", f"${tech.get('current_price', 'N/A')}", f"{change:+.2f}%")
                    with tcol2:
                        st.metric("RSI", tech.get('rsi', 'N/A'), tech.get('rsi_signal', ''))
                    with tcol3:
                        st.metric("Trend", tech.get('trend', 'N/A'))
                    
                    st.markdown(f"**Support:** ${tech.get('support', 'N/A')} | **Resistance:** ${tech.get('resistance', 'N/A')}")
                
                # Why it moved
                st.subheader("💡 Why It Moved")
                st.info(exp.get('explanation', 'No explanation available'))
    
    with col2:
        if st.session_state.last_explanation:
            exp = st.session_state.last_explanation
            
            # News
            st.subheader("📰 Recent News")
            news = exp.get('news', [])
            if news:
                for item in news[:5]:
                    st.markdown(f"**{item.get('title', 'No title')}**")
                    st.caption(f"{item.get('publisher', 'Unknown')} - {item.get('published', '')}")
                    st.markdown("---")
            else:
                st.info("No recent news available")

# ==================== TAB 3: SOCIAL CONTENT STUDIO ====================
with tab3:
    st.header("📱 Social Content Studio")
    st.caption("Generate AI-powered social media content for LinkedIn and X")
    
    scol1, scol2 = st.columns([1, 2])
    
    with scol1:
        st.subheader("🎭 Select Persona")
        personas = st.session_state.controller.get_available_personas()
        selected_persona = st.selectbox("Choose AI Persona", personas)
        
        st.markdown("---")
        st.subheader("📝 Content Type")
        content_type = st.radio("Platform", ["🐦 Twitter Post", "🧵 Twitter Thread", "💼 LinkedIn Post"])
        
        st.markdown("---")
        if st.button("✨ Generate Content", type="primary", key="gen_content"):
            with st.spinner(f"Generating {content_type} as {selected_persona}..."):
                platform_map = {
                    "🐦 Twitter Post": "twitter",
                    "🧵 Twitter Thread": "thread",
                    "💼 LinkedIn Post": "linkedin"
                }
                platform = platform_map[content_type]
                content = st.session_state.controller.generate_social_content(ticker, selected_persona, platform)
                st.session_state.last_social_content = content
    
    with scol2:
        st.subheader("📄 Content Preview")
        
        if st.session_state.last_social_content:
            content = st.session_state.last_social_content
            
            if isinstance(content, dict):
                # Market update format (twitter + linkedin)
                if 'twitter' in content:
                    st.markdown("**🐦 Twitter Version:**")
                    st.code(content['twitter'], language=None)
                if 'linkedin' in content:
                    st.markdown("**💼 LinkedIn Version:**")
                    st.code(content['linkedin'], language=None)
            else:
                # Single content string
                st.code(content, language=None)
            
            st.markdown("---")
            st.caption("💡 Tip: Copy the content above and paste it directly into your social media platform!")
        else:
            st.info("👈 Select a persona and click 'Generate Content' to create social media posts")
    
    # Daily Briefing Section
    st.markdown("---")
    st.subheader("📅 Daily Market Briefing")
    
    brief_col1, brief_col2 = st.columns([1, 2])
    with brief_col1:
        briefing_tickers = st.multiselect(
            "Select tickers for briefing",
            ['AAPL', 'TSLA', 'NVDA', 'GOOGL', 'AMZN', 'META', 'SPY', 'BTC-USD'],
            default=['AAPL', 'TSLA', 'NVDA']
        )
        if st.button("📰 Generate Daily Briefing", key="gen_briefing"):
            with st.spinner("Generating daily briefing..."):
                briefing = st.session_state.controller.generate_daily_briefing(briefing_tickers)
                st.session_state.daily_briefing = briefing
    
    with brief_col2:
        if 'daily_briefing' in st.session_state:
            st.markdown("**📊 Today's Market Briefing:**")
            st.markdown(st.session_state.daily_briefing)

# ==================== TAB 4: BEHAVIORAL COACH ====================
with tab4:
    st.header("🧠 Behavioral Coach")
    st.caption("AI-powered trading psychology monitoring and intervention")
    
    if not st.session_state.initialized:
        st.warning("⚠️ Please initialize the system first (load trades and click Initialize)")
    else:
        sim_col1, sim_col2, sim_col3 = st.columns(3)
        
        with sim_col1:
            st.metric("Current Ticker", ticker)
        
        with sim_col2:
            user_action = st.selectbox("Simulate User Action", [
                'None', 'place_order', 'cancel_order', 'modify_order', 'check_position'
            ])
        
        with sim_col3:
            st.write("")
            run_loop = st.button("▶️ Run Analysis", type="primary", key="run_behavioral")
        
        if run_loop:
            with st.spinner("Running Perceive-Reason-Intervene cycle..."):
                if user_action != 'None':
                    for _ in range(3):
                        st.session_state.controller.user_stream.capture_interaction(user_action)
                
                # Run the FULL analyst loop (market + behavioral)
                result = st.session_state.controller.run_full_analyst_loop(
                    ticker,
                    st.session_state.trades,
                    user_action if user_action != 'None' else None
                )
                
                # Combined Insight (the magic feature!)
                if result.get('combined_insight'):
                    st.markdown("### 🎯 Personalized Insight")
                    st.success(result['combined_insight'])
                
                st.markdown("---")
                
                # Behavioral Analysis
                if result.get('behavioral_analysis'):
                    behavioral = result['behavioral_analysis']
                    
                    st.markdown("### 📡 Perception Layer")
                    perc_col1, perc_col2 = st.columns(2)
                    
                    with perc_col1:
                        st.markdown("**Market State**")
                        st.json(behavioral['perception']['market'])
                    
                    with perc_col2:
                        st.markdown("**User Behavior**")
                        st.json(behavioral['perception']['user'])
                    
                    st.markdown("### 🧠 Cognitive Layer")
                    tilt = behavioral['reasoning']['tilt']
                    st.metric("Tilt Score", f"{tilt.get('tilt_score', 0)}/10")
                    
                    if tilt.get('llm_analysis'):
                        st.info(tilt['llm_analysis'])
                    
                    st.markdown("### 🎯 Action Layer")
                    intervention = behavioral['intervention']
                    
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
st.caption("Built with Gemini 2.0 Flash | Antifragile Mirror v2.0 | Market Intelligence + Behavioral Coach + Social Engine")
