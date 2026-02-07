import google.generativeai as genai
import json
import os

from config import PRIMARY_MODEL

import time
import random

class PsychoAnalyst:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API Key is required")
        genai.configure(api_key=api_key)
        # Using configured primary model
        self.model = genai.GenerativeModel(PRIMARY_MODEL)

    def _generate_with_retry(self, prompt, max_retries=3, base_delay=2):
        """Helper to handle rate limits with exponential backoff"""
        for attempt in range(max_retries):
            try:
                return self.model.generate_content(prompt)
            except Exception as e:
                if "429" in str(e) or "Too Many Requests" in str(e):
                    if attempt < max_retries - 1:
                        # Exponential backoff + jitter
                        sleep_time = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
                        print(f"⚠️ Rate limit hit. Retrying in {sleep_time:.1f}s...")
                        time.sleep(sleep_time)
                        continue
                # If not a rate limit or retries exhausted, re-raise or return error
                if attempt == max_retries - 1:
                    raise e
                raise e

    def analyze_behavior(self, trades_description):
        """
        Analyzes the provided trade history for behavioral biases.
        """
        prompt = f"""
        You are an expert Trading Psychologist and Market Analyst. 
        Your goal is to analyze the following trade history and identify specific behavioral biases (e.g., FOMO, Revenge Trading, Gambler's Fallacy, Loss Aversion).

        Here is the user's recent trade history:
        {json.dumps(trades_description, default=str)}

        Please provide a response in Markdown format with the following sections:
        
        ### 🧠 Psychological Profile
        (A brief summary of the trader's decision-making process based on their 'Entry/Exit Signals' and 'Trade Note' patterns.)

        ### ⚠️ Detected Biases
        (List specific biases found. e.g. "Impulsive trading detected where Trade Note mentioned FOMO and Entry Signal was weak.")

        ### 💡 Actionable Nudges
        (Give 3 specific, constructive tips to improve. Be direct but encouraging.)

        Tone: Professional, insightful, like a high-performance coach.
        """
        
        try:
            response = self._generate_with_retry(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                return "⚠️ **API Limit Reached**: You have hit the free tier rate limit for Gemini. We are backing off to let the API cool down."
            return f"Error connecting to Gemini: {str(e)}"

    def get_realtime_nudge(self, market_state, last_trade):
        """
        Provides a quick "Nudge" based on what the market is doing right now vs user's last action.
        """
        prompt = f"""
        The user just traded {last_trade}. 
        The market is currently {market_state}.
        
        Give a 1-sentence "Nudge" or warning to keep them disciplined. 
        Example: "Market is choppy—don't force a trade just to feel productive."
        """
        try:
            response = self._generate_with_retry(prompt)
            return response.text
        except Exception as e:
            return "Stay disciplined. (System offline)"
