"""
FastAPI Backend for Trading Analyst
Exposes all controller methods as REST API endpoints
"""
from fastapi import FastAPI, HTTPException
print("DEBUG: SERVER STARTING...")
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from antifragile_controller import AntifragileController
import data_manager
import pandas as pd

app = FastAPI(
    title="Trading Analyst API",
    description="AI-Powered Trading Analyst + Behavioral Coach + Social Content Engine",
    version="2.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment")

controller = AntifragileController(api_key)
trades_df = pd.DataFrame()
initialized = False


# ==================== MODELS ====================

class TickerRequest(BaseModel):
    ticker: str

class SocialContentRequest(BaseModel):
    ticker: str
    persona: str
    platform: str = "twitter"

class BriefingRequest(BaseModel):
    tickers: List[str]

class BehavioralRequest(BaseModel):
    ticker: str
    user_action: Optional[str] = None


# ==================== ENDPOINTS ====================

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "initialized": initialized}


@app.post("/api/trades/load-demo")
async def load_demo_trades():
    global trades_df
    trades_df = data_manager.generate_mock_trades(30)
    
    # Map columns to frontend expectations
    # Frontend expects: id, ticker, action, quantity, price, timestamp, PnL, status
    display_df = trades_df.copy()
    display_df = display_df.rename(columns={
        'Date': 'timestamp',
        'Ticker': 'ticker',
        'Side': 'action',
        'Size': 'quantity',
        'Entry Price': 'price',
        'PnL': 'PnL'
    })
    
    # Ensure timestamp is ISO string for JSON serialization
    display_df['timestamp'] = display_df['timestamp'].apply(lambda x: x.isoformat() if hasattr(x, 'isoformat') else str(x))
    
    return {
        "success": True,
        "count": len(trades_df),
        "trades": display_df.to_dict(orient="records")
    }


@app.get("/api/trades")
async def get_trades():
    if trades_df.empty:
        return {"trades": [], "count": 0}
        
    # Map columns to frontend expectations
    display_df = trades_df.copy()
    display_df = display_df.rename(columns={
        'Date': 'timestamp',
        'Ticker': 'ticker',
        'Side': 'action',
        'Size': 'quantity',
        'Entry Price': 'price',
        'PnL': 'PnL'
    })
    
    # Ensure timestamp is ISO string
    display_df['timestamp'] = display_df['timestamp'].apply(lambda x: x.isoformat() if hasattr(x, 'isoformat') else str(x))
    
    return {
        "trades": display_df.to_dict(orient="records"),
        "count": len(trades_df)
    }


@app.get("/api/trades/metrics")
async def get_trade_metrics():
    if trades_df.empty:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "total_pnl": 0
        }
    
    total = len(trades_df)
    wins = len(trades_df[trades_df['PnL'] > 0])
    win_rate = (wins / total * 100) if total > 0 else 0
    total_pnl = trades_df['PnL'].sum()
    
    return {
        "total_trades": total,
        "win_rate": round(win_rate, 1),
        "total_pnl": round(total_pnl, 2)
    }


@app.post("/api/system/initialize")
async def initialize_system():
    global initialized
    if trades_df.empty:
        raise HTTPException(status_code=400, detail="Load trades first")
    
    profile = controller.initialize_trader_profile(trades_df)
    initialized = True
    return {
        "success": True,
        "profile": profile
    }


@app.get("/api/system/status")
async def get_system_status():
    return {
        "initialized": initialized,
        "has_trades": not trades_df.empty,
        "trade_count": len(trades_df) if not trades_df.empty else 0
    }


@app.get("/api/system/diagnostics")
async def get_diagnostics():
    if not initialized:
        return {"error": "System not initialized"}
    return controller.get_system_diagnostics()


@app.post("/api/market/analyze")
async def analyze_market(request: TickerRequest):
    try:
        explanation = controller.explain_market_move(request.ticker)
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market/technicals/{ticker}")
async def get_technicals(ticker: str):
    return controller.get_market_technicals(ticker)


@app.get("/api/market/news/{ticker}")
async def get_news(ticker: str):
    return controller.get_market_news(ticker)


@app.get("/api/personas")
async def get_personas():
    return {
        "personas": controller.get_available_personas()
    }


@app.post("/api/social/generate")
async def generate_social_content(request: SocialContentRequest):
    try:
        content = controller.generate_social_content(
            request.ticker,
            request.persona,
            request.platform
        )
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/briefing/generate")
async def generate_briefing(request: BriefingRequest):
    try:
        briefing = controller.generate_daily_briefing(request.tickers)
        return {"briefing": briefing}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/behavioral/analyze")
async def analyze_behavioral(request: BehavioralRequest):
    global trades_df
    if not initialized:
        raise HTTPException(status_code=400, detail="System not initialized")
    
    try:
        # Simulate user actions if provided
        if request.user_action:
            for _ in range(3):
                controller.user_stream.capture_interaction(request.user_action)
        
        result = controller.run_full_analyst_loop(
            request.ticker,
            trades_df,
            request.user_action
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/trader-profile")
async def get_trader_profile():
    if not initialized:
        return {"error": "System not initialized"}
    return controller.trader_profile


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
