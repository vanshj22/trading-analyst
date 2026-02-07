import pandas as pd
import numpy as np
import yfinance as yf
import datetime

def generate_mock_trades(num_trades=20):
    """
    Generates a synthetic DataFrame of CLOSED trades.
    Each row represents a full round-trip trade (Entry + Exit).
    """
    tickers = ['AAPL', 'TSLA', 'NVDA', 'AMD', 'SPY', 'BTC-USD']
    sides = ['LONG', 'SHORT']
    
    data = []
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=60)
    
    for _ in range(num_trades):
        rand_days = np.random.randint(0, 60)
        entry_date = start_date + datetime.timedelta(days=rand_days)
        ticker = np.random.choice(tickers)
        side = np.random.choice(sides)
        
        # Randomize prices
        base_price = np.random.uniform(100, 1000)
        volatility = np.random.uniform(0.01, 0.05)
        outcome_multiplier = 1 + np.random.choice([volatility, -volatility]) # Win or Loss
        
        entry_price = round(base_price, 2)
        if side == 'LONG':
            exit_price = round(base_price * outcome_multiplier, 2)
        else:
            exit_price = round(base_price * (2 - outcome_multiplier), 2) # Inverse logic for short
            
        size = np.random.randint(1, 100)
        pnl = round((exit_price - entry_price) * size if side == 'LONG' else (entry_price - exit_price) * size, 2)

        # Generate Signals & Notes
        if side == 'LONG':
            entry_signals = ["RSI Divergence", "MACD Crossover", "Support Bounce", "Breakout Re-test", "Golden Cross"]
            exit_signals = ["Target Hit", "Trailing Stop", "RSI Overbought", "Time Stop", "News Event"]
        else:
            entry_signals = ["Bearish Engulfing", "Resistance Rejection", "Head & Shoulders", "Breakdown", "Death Cross"]
            exit_signals = ["Cover at Support", "Stop Loss Hit", "RSI Oversold", "Liquidity Grab", "Sector Rotation"]
            
        entry_signal = np.random.choice(entry_signals)
        exit_signal = np.random.choice(exit_signals)
        
        # Generate a "Trade Note" summary
        notes = [
            "Felt good about this setup, executed clean.",
            "Hesitated on entry, got a bad fill.",
            "Exited too early, left money on the table.",
            "Followed the plan perfectly.",
            "Revenge trade after the last loss (bad idea).",
            "FOMO entry, lucky to get out at breakeven.",
            "Textbook setup, smooth sailing.",
            "Market was choppy, got stopped out on noise."
        ]
        trade_note = np.random.choice(notes) if np.random.random() > 0.2 else "" # 80% chance of note

        data.append({
            'Date': entry_date,
            'Ticker': ticker,
            'Side': side,
            'Entry Price': entry_price,
            'Exit Price': exit_price,
            'Size': size,
            'PnL': pnl,
            'Entry Signal': entry_signal,
            'Exit Signal': exit_signal,
            'Trade Note': trade_note
        })
        
    df = pd.DataFrame(data)
    df = df.sort_values(by='Date').reset_index(drop=True)
    return df

def fetch_market_context(ticker):
    """
    Fetches recent market data and news for context.
    Simple wrapper around yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        
        # Calculate simple momentum
        if len(hist) >= 2:
            change = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
            trend = "UP" if change > 0 else "DOWN"
        else:
            trend = "NEUTRAL"
            change = 0.0

        return {
            'current_price': round(hist['Close'].iloc[-1], 2) if not hist.empty else 0,
            'trend': trend,
            'change_pct': round(change, 2)
        }
    except Exception as e:
        return {'error': str(e)}

def maximize_trade_context(trades_df):
    """
    Enriches the trade list with current market context for the LLM.
    """
    enriched_data = []
    # Limit to last 5 trades for performance/demo speed
    recent_trades = trades_df.tail(5)
    
    for _, row in recent_trades.iterrows():
        context = fetch_market_context(row['Ticker'])
        row_dict = row.to_dict()
        row_dict['Market_Context_Now'] = context
        enriched_data.append(row_dict)
    
    return enriched_data
