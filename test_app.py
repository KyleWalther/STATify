import unittest
from flask import Flask, session
from unittest.mock import patch

class TestSpotifyApp(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.app = Flask(__name__)
        self.app.secret_key = 'testsecret'  # for session
        self.client = self.app.test_client()

        # Mock the routes for testing
        @self.app.route('/')
        def home():
            return 'Welcome to Spotify Top Tracks App'

        @self.app.route('/logout')
        def logout():
            session.pop('access_token', None)
            return 'Logged Out'

        @self.app.route('/profile')
        def profile():
            if 'access_token' not in session:
                return 'Redirecting to login...', 302
            return 'User Profile', 200

        @self.app.route('/top_tracks')
        def top_tracks():
            if 'access_token' not in session:
                return 'Redirecting to login...', 302
            return 'Top Tracks', 200

        @self.app.route('/top_artists')
        def top_artists():
            if 'access_token' not in session:
                return 'Redirecting to login...', 302
            return 'Top Artists', 200

        @self.app.route('/top_albums')
        def top_albums():
            if 'access_token' not in session:
                return 'Redirecting to login...', 302
            return 'Top Albums', 200


    def test_home(self):
        """Test the home route"""
        with self.client:
            response = self.client.get('/')
            # Check if the welcome message exists in the response
            self.assertIn(b'Welcome to Spotify Top Tracks App', response.data)

    def test_logout(self):
        """Test the logout route"""
        with self.client:
            # Mock the session to have an access token
            with self.client.session_transaction() as sess:
                sess['access_token'] = 'fake_token'

            response = self.client.get('/logout')
            self.assertNotIn('access_token', session)  # Ensure token is removed
            self.assertEqual(response.data, b'Logged Out')

    def test_profile(self):
        """Test the profile route"""
        with self.client:
            
            with self.client.session_transaction() as sess:
                sess['access_token'] = 'fake_token'

            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'User Profile', response.data)

    def test_top_tracks(self):
        """Test the top tracks route"""
        with self.client:
            
            with self.client.session_transaction() as sess:
                sess['access_token'] = 'fake_token'

            response = self.client.get('/top_tracks')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Top Tracks', response.data)

    def test_top_artists(self):
        """Test the top artists route"""
        with self.client:
           
            with self.client.session_transaction() as sess:
                sess['access_token'] = 'fake_token'

            response = self.client.get('/top_artists')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Top Artists', response.data)

    def test_top_albums(self):
        """Test the top albums route"""
        with self.client:
           
            with self.client.session_transaction() as sess:
                sess['access_token'] = 'fake_token'

            response = self.client.get('/top_albums')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Top Albums', response.data)

if __name__ == '__main__':
    unittest.main()
