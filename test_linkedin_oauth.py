"""
Unit tests for LinkedIn OAuth Integration
"""
import unittest
from unittest.mock import patch, MagicMock
import os
from linkedin_oauth import LinkedInOAuth

class TestLinkedInOAuth(unittest.TestCase):
    
    def setUp(self):
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"
        self.redirect_uri = "http://localhost:8501"
        self.oauth = LinkedInOAuth(self.client_id, self.client_secret, self.redirect_uri)
        
    def test_get_authorization_url(self):
        url, state = self.oauth.get_authorization_url()
        self.assertIn("response_type=code", url)
        self.assertIn(f"client_id={self.client_id}", url)
        self.assertIn(f"redirect_uri={self.redirect_uri}", url)
        self.assertTrue(len(state) > 0)
        
    @patch('requests.post')
    def test_exchange_code_for_token(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "test_token",
            "expires_in": 3600
        }
        mock_post.return_value = mock_response
        
        token_data = self.oauth.exchange_code_for_token("auth_code")
        self.assertEqual(token_data["access_token"], "test_token")
        
        # Verify request parameters
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['data']['grant_type'], 'authorization_code')
        self.assertEqual(kwargs['data']['code'], 'auth_code')
        
    @patch('requests.get')
    def test_get_user_profile(self, mock_get):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "sub": "test_urn",
            "name": "Test User"
        }
        mock_get.return_value = mock_response
        
        profile = self.oauth.get_user_profile("access_token")
        self.assertEqual(profile["sub"], "test_urn")
        
        # Verify headers
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertIn("Authorization", kwargs['headers'])
        self.assertEqual(kwargs['headers']['Authorization'], "Bearer access_token")

    @patch('requests.post')
    def test_post_text_content(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": "urn:li:share:123"}
        mock_post.return_value = mock_response
        
        response = self.oauth.post_text_content("token", "urn:li:person:123", "Hello World")
        self.assertEqual(response["id"], "urn:li:share:123")
        
        # Verify payload structure
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        payload = kwargs['json']
        self.assertEqual(payload["author"], "urn:li:person:123")
        self.assertEqual(
            payload["specificContent"]["com.linkedin.ugc.ShareContent"]["shareCommentary"]["text"], 
            "Hello World"
        )

if __name__ == '__main__':
    unittest.main()
