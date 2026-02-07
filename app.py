import streamlit as st
import pandas as pd
import data_manager
from analyst_core import PsychoAnalyst
from persona_bot import PersonaBot, PERSONAS
import os

# Page Config
st.set_page_config(
    page_title="AI Trading Analyst",
    page_icon="📈",
    layout="wide"
)

# Title and Intro
st.title("🧠 AI Psycho-Analyst & Content Engine")
st.markdown("""
    **Mission:** Combine market intelligence with behavioral awareness. 
    Analyze your trading psychology or generate persona-based content.
""")

# --- Sidebar ---
st.sidebar.header("Configuration")

# API Key handling
api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Get key from aistudio.google.com")
if not api_key:
    # Try getting from env
    api_key = os.getenv("GEMINI_API_KEY") 

if api_key:
    api_key = api_key.strip() 
    if api_key:
        st.sidebar.success("API Key loaded from environment")
    else:
        st.sidebar.warning("Please enter your Gemini API Key to activate AI features.")

# Demo Data Loader
if st.sidebar.button("Load Demo Trade Data"):
    st.session_state['trades'] = data_manager.generate_mock_trades()
    st.sidebar.success("Demo data loaded!")

if 'trades' not in st.session_state:
    st.session_state['trades'] = pd.DataFrame() # Empty init

# --- Main App ---
tab1, tab2 = st.tabs(["🧠 Trader Psycho-Analysis", "🎭 Social Persona Bot"])

# TAB 1: Analysis
with tab1:
    st.header("Behavioral Analysis")
    
    if st.session_state['trades'].empty:
        st.info("No trade data found. Please load demo data from the sidebar or upload a CSV (feature coming soon).")
    else:
        # Display Data
        st.subheader("Recent Trade Journal")
        st.dataframe(st.session_state['trades'], use_container_width=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("Total Trades", len(st.session_state['trades']))
            last_trade = st.session_state['trades'].iloc[-1]
            st.metric("Last Trade", f"{last_trade['Side']} {last_trade['Ticker']} ({last_trade['PnL']})")
        
        with col2:
            if api_key:
                if st.button("Analyze My Psychology", type="primary"):
                    with st.spinner("Analyzing behavioral patterns..."):
                        analyst = PsychoAnalyst(api_key)
                        # Enrich data for better context
                        analysis_data = data_manager.maximize_trade_context(st.session_state['trades'])
                        result = analyst.analyze_behavior(analysis_data)
                        if "Error" in result:
                            st.error(result)
                        else:
                            st.markdown(result)
            else:
                st.error("API Key required. Please check sidebar settings.")

# TAB 2: Persona Bot
with tab2:
    st.header("AI Social Media Persona")
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        selected_persona = st.selectbox("Choose Persona", list(PERSONAS.keys()))
        topic = st.text_input("Topic / Ticker", value="Tesla Earnings")
        context = st.text_area("Market Context (Optional)", value="Stock is up 5% despite missing revenue estimates.")
    
    with col_p2:
        st.markdown(f"**Current Persona:** *{selected_persona}*")
        st.info(PERSONAS[selected_persona])
        
        if api_key:
            if st.button("Generate Content"):
                with st.spinner("Crafting tweet..."):
                    bot = PersonaBot(api_key)
                    post = bot.generate_post(selected_persona, topic, context)
                    
                    st.success("Generated Content:")
                    st.code(post, language="markdown")
        else:
            st.error("API Key required.")

# Footer
st.markdown("---")
st.caption("Built with Streamlit & Gemini 2.0 Flash")
