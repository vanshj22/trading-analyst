"""
LinkedIn OAuth 2.0 Integration Module
Handles authentication flow and API interactions for sharing content.
"""
import requests
import urllib.parse
import os
import secrets
from typing import Dict, Optional, Tuple

class LinkedInOAuth:
    """
    Handles LinkedIn OAuth 2.0 authentication flow and API interactions.
    Implements 3-legged OAuth for user-authorized posting.
    """
    
    AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
    ACCESS_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
    API_BASE_URL = "https://api.linkedin.com/v2"
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = "w_member_social openid profile email" # Scopes needed for posting & ID
        
    def get_authorization_url(self) -> Tuple[str, str]:
        """
        Generates the authorization URL for the user to visit.
        Returns: (auth_url, state_token)
        """
        state = secrets.token_urlsafe(16)
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "state": state,
            "scope": self.scope
        }
        
        url_parts = list(urllib.parse.urlparse(self.AUTHORIZATION_URL))
        url_parts[4] = urllib.parse.urlencode(params)
        return urllib.parse.urlunparse(url_parts), state

    def exchange_code_for_token(self, authorization_code: str) -> Dict:
        """
        Exchanges the authorization code for an access token.
        """
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        
        response = requests.post(self.ACCESS_TOKEN_URL, data=data, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Token exchange failed: {response.text}")
            
        return response.json()

    def get_user_profile(self, access_token: str) -> Dict:
        """
        Fetches the authenticated user's profile information (URN).
        Uses the 'me' endpoint or 'userinfo' depending on scopes.
        With 'openid' scope, we use userinfo endpoint.
        """
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Using OpenID Connect endpoint for basic profile info
        response = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
        
        if response.status_code != 200:
            # Fallback to legacy v2/me if openid fails or not available
            response = requests.get(f"{self.API_BASE_URL}/me", headers=headers)
            
        if response.status_code != 200:
            raise Exception(f"Failed to fetch profile: {response.text}")
            
        return response.json()

    def post_text_content(self, access_token: str, person_urn: str, text: str) -> Dict:
        """
        Posts text content to LinkedIn profile.
        Requires 'w_member_social' scope.
        """
        url = f"{self.API_BASE_URL}/ugcPosts"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        # Ensure URN is in correct format (adding 'urn:li:person:' if missing)
        # Note: OpenID 'sub' is the ID, needs prefix for URN
        if not person_urn.startswith("urn:li:"):
            author_urn = f"urn:li:person:{person_urn}"
        else:
            author_urn = person_urn

        post_data = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        response = requests.post(url, json=post_data, headers=headers)
        
        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to post to LinkedIn: {response.text}")
            
        return response.json()
