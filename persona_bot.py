"""
Social Content Engine: AI Persona-Based Content Generation
Generates platform-appropriate content for LinkedIn and X (Twitter)
"""
import google.generativeai as genai
from typing import Dict, Optional
from datetime import datetime


from config import PRIMARY_MODEL

# Enhanced Persona Definitions with Platform-Specific Styles
PERSONAS = {
    "The Quantitative Stoic": {
        "description": "You are a cold, data-driven quant. You speak in probabilities, ignore emotion, and use technical terms correctly. You despise hype.",
        "twitter_style": "Brief, analytical, aloof. Use precise numbers. No emojis. End with a dry observation.",
        "linkedin_style": "Professional, data-heavy, includes methodology. Reference statistical concepts. Structured with bullet points.",
        "voice": "calm, measured, slightly condescending to retail traders"
    },
    "The Hype Momentum Trader": {
        "description": "You are an excited momentum trader who uses lots of emojis (🚀, 💎, 📈). You chase trends, speak in memes, and are very energetic.",
        "twitter_style": "Hype, loud, community-focused. Use emojis liberally. Reference 'we' and the community. End with a call to action.",
        "linkedin_style": "Energetic but professional. Use emojis sparingly. Focus on opportunity and timing. Include a question to drive engagement.",
        "voice": "excited, FOMO-inducing, uses trading slang"
    },
    "The Contrarian Value Investor": {
        "description": "You are a cynical deep-value investor. You think everything is a bubble. You quote Buffett and Munger. You are patient and slightly condescending.",
        "twitter_style": "Grumpy, wise, long-term. Use quotes from legendary investors. Dismiss short-term noise. End with a wisdom bomb.",
        "linkedin_style": "Thoughtful, historical perspective. Reference past market cycles. Include a lesson learned. Formal but accessible.",
        "voice": "patient, wise, slightly grumpy about market speculation"
    },
    "The Technical Analyst": {
        "description": "You are a chart obsessed technician. You see patterns everywhere. You reference RSI, MACD, support/resistance. You believe price tells all.",
        "twitter_style": "Pattern-focused, uses chart terms. Reference specific levels. End with 'watching for...' statements.",
        "linkedin_style": "Educational, explains patterns for beginners. Uses proper TA terminology. Includes what to watch for.",
        "voice": "methodical, pattern-seeking, confident in charts"
    },
    "The Macro Strategist": {
        "description": "You see the big picture. Central banks, geopolitics, currency flows - you connect everything. Individual stocks are just pieces of a larger puzzle.",
        "twitter_style": "Connect multiple data points. Reference Fed, global events. Think in themes not tickers. End with a macro insight.",
        "linkedin_style": "Thought leadership style. Connect global events to market moves. Use frameworks. Reference economic indicators.",
        "voice": "intellectual, connecting dots, globally aware"
    }
}


class PersonaBot:
    """
    Enhanced Social Content Engine with multi-platform support.
    Generates content appropriate for LinkedIn (professional) and X (concise).
    """
    
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API Key is required")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(PRIMARY_MODEL)
        self.content_history = []

    def get_available_personas(self) -> list:
        """Returns list of available persona names."""
        return list(PERSONAS.keys())

    def generate_twitter_post(self, persona_name: str, topic: str, market_context: str = "") -> str:
        """
        Generates a single Twitter/X post (under 280 characters).
        """
        persona = PERSONAS.get(persona_name, PERSONAS["The Quantitative Stoic"])
        
        prompt = f"""You are: {persona['description']}

Style for Twitter: {persona['twitter_style']}
Voice: {persona['voice']}

Topic: {topic}
Market Context: {market_context}

Write a single Twitter/X post.
STRICT CONSTRAINTS:
- MUST be under 280 characters
- Use 1-2 relevant hashtags
- Stay perfectly in character
- No preamble like "Here is a tweet" - just the tweet text
- Make it engaging and shareable"""

        return self._generate_content(prompt, "twitter")

    def generate_twitter_thread(self, persona_name: str, topic: str, market_context: str = "", num_tweets: int = 4) -> str:
        """
        Generates a Twitter thread (multiple connected tweets).
        """
        persona = PERSONAS.get(persona_name, PERSONAS["The Quantitative Stoic"])
        
        prompt = f"""You are: {persona['description']}

Style for Twitter: {persona['twitter_style']}
Voice: {persona['voice']}

Topic: {topic}
Market Context: {market_context}

Write a Twitter thread of {num_tweets} tweets.
CONSTRAINTS:
- Number each tweet (1/, 2/, etc.)
- Each tweet MUST be under 280 characters
- First tweet should hook the reader
- Middle tweets provide substance
- Last tweet should have a takeaway or call to engagement
- Use hashtags only in the last tweet
- Stay perfectly in character throughout
- No preamble - just the thread"""

        return self._generate_content(prompt, "thread")

    def generate_linkedin_post(self, persona_name: str, topic: str, market_context: str = "") -> str:
        """
        Generates a professional LinkedIn post (longer form).
        """
        persona = PERSONAS.get(persona_name, PERSONAS["The Quantitative Stoic"])
        
        prompt = f"""You are: {persona['description']}

Style for LinkedIn: {persona['linkedin_style']}
Voice: {persona['voice']}

Topic: {topic}
Market Context: {market_context}

Write a LinkedIn post.
CONSTRAINTS:
- 150-300 words
- Professional but accessible
- Use line breaks for readability
- Include a thought-provoking question or call to discussion at the end
- Use 3-5 relevant hashtags at the very end
- Stay in character but adapt for professional audience
- No preamble - just the post content"""

        return self._generate_content(prompt, "linkedin")

    def generate_market_update(self, persona_name: str, ticker: str, technicals: Dict, news: list) -> Dict:
        """
        Generates both Twitter and LinkedIn versions of a market update.
        """
        # Build context from data
        context_parts = []
        if technicals and 'error' not in technicals:
            context_parts.append(
                f"Price: ${technicals.get('current_price', 'N/A')} "
                f"({technicals.get('price_change_1d', 0):+.2f}% today). "
                f"RSI: {technicals.get('rsi', 'N/A')} ({technicals.get('rsi_signal', '')}). "
                f"Trend: {technicals.get('trend', 'N/A')}."
            )
        
        if news:
            headlines = " | ".join([n['title'] for n in news[:3]])
            context_parts.append(f"News: {headlines}")
        
        market_context = " ".join(context_parts)
        topic = f"{ticker} market update"
        
        twitter = self.generate_twitter_post(persona_name, topic, market_context)
        linkedin = self.generate_linkedin_post(persona_name, topic, market_context)
        
        return {
            'ticker': ticker,
            'persona': persona_name,
            'twitter': twitter,
            'linkedin': linkedin,
            'generated_at': datetime.now().isoformat()
        }

    def generate_daily_briefing_social(self, briefing_text: str, persona_name: str) -> Dict:
        """
        Transforms a market briefing into social media posts.
        """
        topic = "Daily Market Briefing"
        
        twitter = self.generate_twitter_thread(persona_name, topic, briefing_text, num_tweets=3)
        linkedin = self.generate_linkedin_post(persona_name, topic, briefing_text)
        
        return {
            'twitter_thread': twitter,
            'linkedin_post': linkedin,
            'persona': persona_name,
            'generated_at': datetime.now().isoformat()
        }

    def _generate_content(self, prompt: str, content_type: str) -> str:
        """Internal method to generate content with error handling."""
        try:
            response = self.model.generate_content(prompt)
            content = response.text
            
            # Log for history
            self.content_history.append({
                'type': content_type,
                'content': content[:100] + '...',
                'timestamp': datetime.now().isoformat()
            })
            
            return content
        except Exception as e:
            if "429" in str(e):
                return "⚠️ **Error**: API Rate Limit Exceeded. Please wait a moment."
            return f"Error generating content: {str(e)}"

    def get_content_history(self, limit: int = 10) -> list:
        """Returns recent content generation history."""
        return self.content_history[-limit:]

    def post_to_linkedin(self, content: str, access_token: str, person_urn: str) -> Dict:
        """
        Posts the generated content to LinkedIn using the provided access token.
        
        Args:
            content (str): The text content to post
            access_token (str): Valid LinkedIn OAuth access token
            person_urn (str): The user's LinkedIn URN (e.g., 'urn:li:person:...')
            
        Returns:
            Dict: API response from LinkedIn
        """
        try:
            # We import here to avoid circular dependencies if any, 
            # and because this is a specific integration feature
            from linkedin_oauth import LinkedInOAuth
            import os
            
            # Initialize OAuth client just for posting (we don't need auth flow here)
            # We need client_id/secret for initialization but won't use them for posting
            client_id = os.getenv("LINKEDIN_CLIENT_ID")
            client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
            
            if not client_id or not client_secret:
                return {"error": "LinkedIn credentials not found in environment"}
                
            # Redirect URI not needed for posting, passing empty string
            oauth = LinkedInOAuth(client_id, client_secret, "") 
            
            return oauth.post_text_content(access_token, person_urn, content)
        except Exception as e:
            return {"error": str(e)}


# Legacy compatibility - keep old function signature working
def generate_post(persona_name: str, topic: str, market_context: str = "", api_key: str = None) -> str:
    """Legacy function for backwards compatibility."""
    if not api_key:
        return "Error: API key required"
    bot = PersonaBot(api_key)
    return bot.generate_twitter_post(persona_name, topic, market_context)
