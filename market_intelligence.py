"""
Market Intelligence Layer: Deep Market Analysis
Fetches news, calculates technicals, and explains market moves using LLM
"""
import yfinance as yf
import pandas as pd
import numpy as np
import google.generativeai as genai
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class MarketIntelligence:
    """
    Provides deep market analysis including:
    - News fetching and summarization
    - Technical indicator calculation
    - LLM-powered "Why it moved" explanations
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        self.cache = {}  # Simple cache to avoid redundant API calls
        self._last_request_time = 0

    def _generate_content_with_retry(self, prompt: str) -> str:
        """Internal method to handle rate limits with retries."""
        import time
        
        # Simple cache check
        cache_key = hash(prompt)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Enforce minimum delay between requests (2 seconds)
        current_time = time.time()
        if current_time - self._last_request_time < 2:
            time.sleep(2)
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                self._last_request_time = time.time()
                result = response.text
                
                # Cache successful result
                self.cache[cache_key] = result
                return result
                
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    if attempt < max_retries - 1:
                        sleep_time = 2 ** (attempt + 1)  # Exponential backoff: 2s, 4s, 8s
                        time.sleep(sleep_time)
                        continue
                    else:
                        raise e
                else:
                    raise e

    def _generate_static_explanation(self, ticker: str, technicals: Dict, news: list) -> str:
        """Generates a static explanation when LLM is unavailable (rate limited, etc.)."""
        price = technicals.get('current_price', 'N/A')
        change_1d = technicals.get('price_change_1d', 0)
        change_5d = technicals.get('price_change_5d', 0)
        trend = technicals.get('trend', 'NEUTRAL')
        rsi = technicals.get('rsi', 50)
        rsi_signal = technicals.get('rsi_signal', 'NEUTRAL')
        volume = technicals.get('volume_signal', 'NORMAL')
        support = technicals.get('support', 'N/A')
        resistance = technicals.get('resistance', 'N/A')
        
        # Build explanation based on data
        direction = "up" if change_1d > 0 else "down" if change_1d < 0 else "flat"
        
        explanation_parts = []
        
        # Price movement
        explanation_parts.append(
            f"{ticker} moved {direction} {abs(change_1d):.2f}% today, trading at ${price}."
        )
        
        # Trend context
        if trend == "BULLISH":
            explanation_parts.append("The stock is in a bullish trend, trading above both SMA20 and SMA50.")
        elif trend == "BEARISH":
            explanation_parts.append("The stock is in a bearish trend, trading below both SMA20 and SMA50.")
        else:
            explanation_parts.append("The stock is showing mixed signals between short and long-term moving averages.")
        
        # RSI insight
        if rsi_signal == "OVERBOUGHT":
            explanation_parts.append(f"RSI at {rsi:.1f} indicates overbought conditions - potential pullback ahead.")
        elif rsi_signal == "OVERSOLD":
            explanation_parts.append(f"RSI at {rsi:.1f} indicates oversold conditions - potential bounce possible.")
        
        # Volume
        if volume == "HIGH":
            explanation_parts.append("Elevated volume suggests strong conviction behind the move.")
        
        # News mention
        if news and len(news) > 0:
            top_headline = news[0].get('title', '')
            if top_headline:
                explanation_parts.append(f"Recent headline: \"{top_headline}\"")
        
        # Key levels
        explanation_parts.append(f"Key levels to watch: Support at ${support}, Resistance at ${resistance}.")
        
        return " ".join(explanation_parts)

    def fetch_news(self, ticker: str, max_items: int = 5) -> List[Dict]:
        """
        Fetches recent news headlines for a given ticker using yfinance.
        Returns a list of news items with title, publisher, and link.
        """
        try:
            stock = yf.Ticker(ticker)
            news = stock.news[:max_items] if stock.news else []
            
            formatted_news = []
            for item in news:
                formatted_news.append({
                    'title': item.get('title', 'No title'),
                    'publisher': item.get('publisher', 'Unknown'),
                    'link': item.get('link', '#'),
                    'published': datetime.fromtimestamp(
                        item.get('providerPublishTime', 0)
                    ).strftime('%Y-%m-%d %H:%M') if item.get('providerPublishTime') else 'Unknown'
                })
            
            return formatted_news
        except Exception as e:
            return [{'title': f'Error fetching news: {str(e)}', 'publisher': 'System', 'link': '#'}]

    def calculate_technicals(self, ticker: str) -> Dict:
        """
        Calculates basic technical indicators:
        - RSI (14-period)
        - SMA 20 vs SMA 50 (trend)
        - Volume analysis
        - Support/Resistance levels
        """
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="3mo", interval="1d")
            
            if hist.empty or len(hist) < 20:
                return {'error': 'Insufficient data for technical analysis'}
            
            close = hist['Close']
            volume = hist['Volume']
            
            # RSI Calculation
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1]
            
            # Moving Averages
            sma_20 = close.rolling(window=20).mean().iloc[-1]
            sma_50 = close.rolling(window=50).mean().iloc[-1] if len(close) >= 50 else sma_20
            
            # Trend determination
            if close.iloc[-1] > sma_20 > sma_50:
                trend = "BULLISH"
            elif close.iloc[-1] < sma_20 < sma_50:
                trend = "BEARISH"
            else:
                trend = "NEUTRAL"
            
            # Volume Analysis
            avg_volume = volume.mean()
            current_volume = volume.iloc[-1]
            volume_signal = "HIGH" if current_volume > avg_volume * 1.5 else "NORMAL"
            
            # Simple Support/Resistance (last 20 days high/low)
            recent = hist.tail(20)
            resistance = recent['High'].max()
            support = recent['Low'].min()
            current_price = close.iloc[-1]
            
            # Price change
            price_change_1d = ((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]) * 100
            price_change_5d = ((close.iloc[-1] - close.iloc[-5]) / close.iloc[-5]) * 100 if len(close) >= 5 else 0
            
            return {
                'current_price': round(current_price, 2),
                'rsi': round(current_rsi, 2),
                'rsi_signal': 'OVERBOUGHT' if current_rsi > 70 else ('OVERSOLD' if current_rsi < 30 else 'NEUTRAL'),
                'sma_20': round(sma_20, 2),
                'sma_50': round(sma_50, 2),
                'trend': trend,
                'volume_signal': volume_signal,
                'support': round(support, 2),
                'resistance': round(resistance, 2),
                'price_change_1d': round(price_change_1d, 2),
                'price_change_5d': round(price_change_5d, 2),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}

    def explain_market_move(self, ticker: str) -> Dict:
        """
        Uses LLM to synthesize Price + News + Technicals into a 
        "Why it moved" explanation. This is the core analyst feature.
        """
        # Fetch all data
        news = self.fetch_news(ticker)
        technicals = self.calculate_technicals(ticker)
        
        # If yfinance fails, use demo data for hackathon demo
        if 'error' in technicals:
            technicals = self._get_demo_technicals(ticker)
            news = self._get_demo_news(ticker)
        
        # Prepare news summary for LLM
        news_summary = "\n".join([
            f"- {item['title']} ({item['publisher']})" 
            for item in news[:5]
        ]) if news else "No recent news available."
        
        prompt = f"""You are a professional market analyst. Explain why {ticker} moved today.

PRICE ACTION:
- Current Price: ${technicals['current_price']}
- 1-Day Change: {technicals['price_change_1d']}%
- 5-Day Change: {technicals['price_change_5d']}%

TECHNICAL INDICATORS:
- RSI (14): {technicals['rsi']} ({technicals['rsi_signal']})
- Trend: {technicals['trend']} (Price vs SMA20 vs SMA50)
- Volume: {technicals['volume_signal']}
- Support: ${technicals['support']} | Resistance: ${technicals['resistance']}

RECENT NEWS:
{news_summary}

Provide:
1. A concise 2-3 sentence explanation of WHY the price moved
2. Key drivers (news, technicals, or sentiment)
3. What traders should watch next

Keep it professional but accessible. No predictions or buy/sell signals."""

        try:
            explanation = self._generate_content_with_retry(prompt)
            
            return {
                'ticker': ticker,
                'explanation': explanation,
                'technicals': technicals,
                'news': news,
                'generated_at': datetime.now().isoformat()
            }
        except Exception as e:
            # Use static fallback when LLM fails (rate limited, etc.)
            static_explanation = self._generate_static_explanation(ticker, technicals, news)
            return {
                'ticker': ticker,
                'explanation': static_explanation,
                'technicals': technicals,
                'news': news,
                'generated_at': datetime.now().isoformat(),
                'fallback_mode': True  # Flag to indicate this is a static explanation
            }

    def get_market_sentiment(self, ticker: str) -> Dict:
        """
        Analyzes overall market sentiment based on technicals and news tone.
        """
        technicals = self.calculate_technicals(ticker)
        news = self.fetch_news(ticker)
        
        if 'error' in technicals:
            return {'sentiment': 'UNKNOWN', 'confidence': 0}
        
        prompt = f"""Analyze the sentiment for {ticker} based on:

TECHNICALS:
- RSI: {technicals['rsi']} ({technicals['rsi_signal']})
- Trend: {technicals['trend']}
- 1-Day Change: {technicals['price_change_1d']}%

NEWS HEADLINES:
{chr(10).join([f"- {n['title']}" for n in news[:5]])}

Respond in JSON format:
{{
    "sentiment": "BULLISH|BEARISH|NEUTRAL",
    "confidence": 0-100,
    "key_factors": ["factor1", "factor2"],
    "risk_level": "LOW|MEDIUM|HIGH"
}}"""

        try:
            response = self.model.generate_content(prompt)
            return {
                'raw_response': response.text,
                'technicals_summary': {
                    'rsi': technicals['rsi'],
                    'trend': technicals['trend'],
                    'price_change': technicals['price_change_1d']
                }
            }
        except Exception as e:
            return {'error': str(e)}

    def generate_daily_briefing(self, tickers: List[str]) -> str:
        """
        Generates a comprehensive daily market briefing for multiple tickers.
        """
        briefing_data = []
        
        for ticker in tickers[:5]:  # Limit to 5 tickers
            technicals = self.calculate_technicals(ticker)
            if 'error' not in technicals:
                briefing_data.append({
                    'ticker': ticker,
                    'price': technicals['current_price'],
                    'change': technicals['price_change_1d'],
                    'trend': technicals['trend'],
                    'rsi': technicals['rsi']
                })
        
        if not briefing_data:
            return "Unable to generate briefing. No valid data available."
        
        data_summary = "\n".join([
            f"- {d['ticker']}: ${d['price']} ({d['change']:+.2f}%) | {d['trend']} | RSI: {d['rsi']}"
            for d in briefing_data
        ])
        
        prompt = f"""You are a professional market analyst. Generate a morning market briefing.

TODAY'S DATA:
{data_summary}

Create a 3-paragraph briefing that:
1. Opens with overall market tone
2. Highlights the most significant movers and why
3. Ends with what to watch today

Style: Professional, concise, no predictions. Suitable for LinkedIn or newsletter."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating briefing: {str(e)}"
    
    def _get_demo_technicals(self, ticker: str) -> Dict:
        """Returns demo technical data when yfinance is unavailable."""
        import random
        
        # Generate realistic-looking demo data
        base_prices = {
            'AAPL': 185.50, 'TSLA': 248.30, 'NVDA': 875.20, 'GOOGL': 175.80,
            'AMZN': 185.60, 'META': 520.40, 'SPY': 520.15, 'BTC-USD': 97500.0
        }
        
        base_price = base_prices.get(ticker, 100.0)
        price_change = random.uniform(-3.5, 3.5)
        current_price = base_price * (1 + price_change / 100)
        rsi = random.uniform(35, 65)
        
        return {
            'current_price': round(current_price, 2),
            'rsi': round(rsi, 2),
            'rsi_signal': 'OVERBOUGHT' if rsi > 70 else ('OVERSOLD' if rsi < 30 else 'NEUTRAL'),
            'sma_20': round(current_price * 0.98, 2),
            'sma_50': round(current_price * 0.95, 2),
            'trend': 'BULLISH' if price_change > 0.5 else ('BEARISH' if price_change < -0.5 else 'NEUTRAL'),
            'volume_signal': random.choice(['NORMAL', 'HIGH']),
            'support': round(current_price * 0.95, 2),
            'resistance': round(current_price * 1.05, 2),
            'price_change_1d': round(price_change, 2),
            'price_change_5d': round(price_change * 1.5, 2),
            'timestamp': datetime.now().isoformat(),
            'demo_mode': True  # Flag to indicate this is demo data
        }
    
    def _get_demo_news(self, ticker: str) -> List[Dict]:
        """Returns demo news when yfinance is unavailable."""
        demo_news = {
            'AAPL': [
                {'title': 'Apple announces new AI features for iPhone', 'publisher': 'TechCrunch', 'link': '#', 'published': 'Today'},
                {'title': 'Apple stock hits new highs amid services growth', 'publisher': 'Bloomberg', 'link': '#', 'published': 'Today'},
            ],
            'TSLA': [
                {'title': 'Tesla expands Supercharger network globally', 'publisher': 'Reuters', 'link': '#', 'published': 'Today'},
                {'title': 'EV demand remains strong in Q4', 'publisher': 'CNBC', 'link': '#', 'published': 'Today'},
            ],
            'NVDA': [
                {'title': 'NVIDIA AI chips see unprecedented demand', 'publisher': 'WSJ', 'link': '#', 'published': 'Today'},
                {'title': 'Data center revenue exceeds expectations', 'publisher': 'Bloomberg', 'link': '#', 'published': 'Today'},
            ],
        }
        
        return demo_news.get(ticker, [
            {'title': f'{ticker} shows mixed signals in volatile market', 'publisher': 'MarketWatch', 'link': '#', 'published': 'Today'},
            {'title': f'Analysts update outlook for {ticker}', 'publisher': 'Seeking Alpha', 'link': '#', 'published': 'Today'},
        ])
