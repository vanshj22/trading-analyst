import data_manager
import pandas as pd

try:
    print("Generating mock trades...")
    df = data_manager.generate_mock_trades(5)
    print("Columns:", df.columns.tolist())
    print("First row data:")
    print(df.iloc[0].to_dict())
    
    print("\nVerifying maximize_trade_context...")
    # Mocking fetch_market_context to avoid network calls or errors if yfinance fails
    def mock_fetch(ticker):
        return {'current_price': 150, 'trend': 'UP', 'change_pct': 1.5}
    
    # Temporarily monkeypatch
    original_fetch = data_manager.fetch_market_context
    data_manager.fetch_market_context = mock_fetch
    
    enriched = data_manager.maximize_trade_context(df)
    print("Enriched first row keys:", enriched[0].keys())
    
    print("\nValidation Successful.")
except Exception as e:
    print(f"\nValidation Failed: {e}")
