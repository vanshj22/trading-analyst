import google.generativeai as genai

PERSONAS = {
    "The Quantitative Stoic": "You are a cold, data-driven quant. You speak in probabilities, ignore emotion, and use technical terms correctly. You despise hype. Style: Brief, analytical, aloof.",
    "The Hype Momentum Trader": "You are an excited momentum trader who uses lots of emojis (🚀, 💎). You chase trends, speak in memes, and are very energetic. Style: Hype, loud, community-focused.",
    "The Contrarian Value Investor": "You are a cynical deep-value investor. You think everything is a bubble. You quote Buffett and Munger. You are patient and slightly condescending to day traders. Style: Grumpy, wise, long-term."
}

class PersonaBot:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API Key is required")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')

    def generate_post(self, persona_name, topic, market_context=""):
        """
        Generates a social media post based on the selected persona.
        """
        system_prompt = PERSONAS.get(persona_name, PERSONAS["The Quantitative Stoic"])
        
        prompt = f"""
        Role: {system_prompt}
        
        Task: Write a Twitter/X post about: {topic}.
        Context: {market_context}
        
        Constraints:
        - Under 280 characters.
        - Use appropriate hashtags.
        - maintain character perfectly.
        - Do not include "Here is a tweet" preamble, just the tweet text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                return "⚠️ **Error**: API Rate Limit Exceeded. Please wait a moment."
            return f"Error generating content: {str(e)}"
