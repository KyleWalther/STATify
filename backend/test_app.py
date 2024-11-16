from unittest.mock import patch
import unittest
from app import app
from flask import session

class AppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configure the app for testing
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret'
        cls.client = app.test_client()

    def test_home_route(self):
        """Test the home page route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Spotify Login Page', response.data)  

    def test_login_route(self):
        """Test the login route redirects to Spotify authorization URL."""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'https://accounts.spotify.com/authorize', response.location.encode())

    def test_callback_route_no_code(self):
        """Test the callback route without an authorization code."""
        response = self.client.get('/callback')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Authorization code not received', response.data)

    def test_top_tracks_route_unauthorized(self):
        """Test the top tracks route when user is not logged in."""
        response = self.client.get('/top_tracks')
        self.assertEqual(response.status_code, 302)  # Expect a redirect if not authenticated
        self.assertIn(b'/login', response.location.encode())  # Updated to check for login redirection

    def test_top_artists_route_unauthorized(self):
        """Test the top artists route when user is not logged in."""
        response = self.client.get('/top_artists')
        self.assertEqual(response.status_code, 302)  
        self.assertIn(b'/login', response.location.encode())  

    def test_logout_route(self):
        """Test the logout route clears the session and redirects to home."""
        with self.client as client:
            # Simulate a logged-in session
            with client.session_transaction() as sess:
                sess['access_token'] = 'test_token'

            response = client.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'access_token', session)
            self.assertIn(b'Welcome to the Spotify Login Page', response.data) 


if __name__ == '__main__':
    unittest.main()

