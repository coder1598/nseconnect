import unittest
import requests
import time
import sys
import os
from datetime import datetime as dt
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from nsetools.ua import Session
from nsetools import urls

class TestSession(unittest.TestCase):
    def setUp(self):
        self.session = Session(session_refresh_interval=2)  # Short interval for testing

    def test_session_headers(self):
        """Test if proper headers are set"""
        headers = self.session.nse_headers()
        essential_headers = [
            "Accept", "Accept-Language", "user-agent", "X-Requested-With"
        ]
        for header in essential_headers:
            self.assertIn(header, headers)
        self.assertIsInstance(headers, dict)

    def test_session_creation(self):
        """Test if session is created with proper attributes"""
        self.assertIsInstance(self.session._session, requests.Session)
        self.assertIsInstance(self.session._session_init_time, dt)
        self.assertEqual(self.session.session_refresh_interval, 2)

    def test_session_refresh(self):
        """Test if session refreshes after interval"""
        # Create session with very short interval
        self.session = Session(session_refresh_interval=1)
        
        initial_time = self.session._session_init_time
        
        # Wait longer than refresh interval
        time.sleep(2)  # Wait longer than refresh interval
        
        # Explicitly create a new session
        self.session.create_session()
        
        # Verify timestamp was updated (this is more reliable than comparing object IDs)
        self.assertNotEqual(initial_time, self.session._session_init_time)
        self.assertGreater(self.session._session_init_time, initial_time)

    def test_session_reuse(self):
        """Test if session is reused within refresh interval"""
        response1 = self.session.fetch(urls.NSE_HOME)
        initial_time = self.session._session_init_time
        
        response2 = self.session.fetch(urls.NSE_HOME)
        self.assertEqual(initial_time, self.session._session_init_time)
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_cache_hit(self):
        """Test if responses are cached and reused"""
        # First request should hit network
        response1 = self.session.fetch(urls.NSE_HOME)
        self.assertEqual(response1.status_code, 200)
        
        # Second request should hit cache
        response2 = self.session.fetch(urls.NSE_HOME)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response1, response2)  # Same response object
        
        # Both responses should be in cache
        self.assertIn(urls.NSE_HOME, Session.__CACHE__)

    def test_cache_expiry(self):
        """Test if cache expires after timeout"""
        self.session.cache_timeout = 2  # Set short timeout for testing
        
        # First request
        response1 = self.session.fetch(urls.NSE_HOME)
        self.assertEqual(response1.status_code, 200)
        
        # Wait for cache to expire
        time.sleep(3)
        
        # Second request should hit network again
        response2 = self.session.fetch(urls.NSE_HOME)
        self.assertEqual(response2.status_code, 200)
        self.assertNotEqual(id(response1), id(response2))  # Different response objects

    def test_cache_flush(self):
        """Test if cache flush clears all cached responses"""
        # Cache a response
        response = self.session.fetch(urls.NSE_HOME)
        self.assertIn(urls.NSE_HOME, Session.__CACHE__)
        
        # Flush cache
        self.session.flush()
        self.assertEqual(len(Session.__CACHE__), 0)

if __name__ == '__main__':
    unittest.main()
