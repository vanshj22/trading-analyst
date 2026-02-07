"""
Manual Verification Script for LinkedIn OAuth
"""
import requests
from unittest.mock import MagicMock
from linkedin_oauth import LinkedInOAuth
import sys

def verify_linkedin_logic():
    print("🚀 Starting LinkedIn OAuth Logic Verification")
    
    # 1. Setup
    client_id = "test_client"
    client_secret = "test_secret"
    redirect_uri = "http://localhost:8501"
    
    oauth = LinkedInOAuth(client_id, client_secret, redirect_uri)
    print("✅ OAuth Client Initialized")
    
    # 2. Test Authorization URL
    url, state = oauth.get_authorization_url()
    print(f"\n📋 Authorization URL Generated: {url[:50]}...")
    if "response_type=code" in url and client_id in url:
        print("✅ Auth URL parameters verified")
    else:
        print("❌ Auth URL parameters missing")
        
    # 3. Test Token Exchange (with mocking)
    print("\n🔄 Testing Token Exchange Logic...")
    
    # Mock requests.post
    original_post = requests.post
    
    try:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "mock_token_123"}
        
        requests.post = MagicMock(return_value=mock_response)
        
        token = oauth.exchange_code_for_token("auth_code_123")
        
        if token['access_token'] == "mock_token_123":
            print("✅ Token exchange logic verified")
        else:
            print(f"❌ Token exchange failed. Got: {token}")
            
    except Exception as e:
        print(f"❌ Error in token exchange: {e}")
    finally:
        requests.post = original_post

    # 4. Test Posting Logic (with mocking)
    print("\n📢 Testing Posting Logic...")
    original_post = requests.post
    
    try:
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": "urn:li:share:test"}
        
        requests.post = MagicMock(return_value=mock_response)
        
        resp = oauth.post_text_content("mock_token", "urn:li:person:user123", "Test Post")
        
        # Check payload
        call_args = requests.post.call_args
        if call_args:
            payload = call_args[1]['json']
            text = payload["specificContent"]["com.linkedin.ugc.ShareContent"]["shareCommentary"]["text"]
            if text == "Test Post":
                print(f"✅ Post payload verified. Content: '{text}'")
            else:
                 print(f"❌ Post payload mismatch. Got: '{text}'")
        
    except Exception as e:
         print(f"❌ Error in posting: {e}")
    finally:
        requests.post = original_post
        
    print("\n✨ Verification Complete!")

if __name__ == "__main__":
    verify_linkedin_logic()
