# STATify

the title of my site is STATify (this may be changed upon extension request results via Spotify).

My website integrates with the Spotify API to gather user data and display it across multiple pages, providing unique insights into the user's listening history. Once signed in successfully, users can explore their saved playlists, top tracks, artists, and albums, all conveniently organized in one place. To enhance the experience, I intorduced a timeframe selection feature, enabling users to view their listening history based on different periods, such as short-term, medium-term, or long-term. Each timeframe will present detailed data, including album or artist images, track names, artist names, album titles, and a ranked list showcasing the top 50 entries from their personal listening history. This feature aims to provide users with a comprehensive and visually engaging view of their music preferences over time.

This test suite is designed to validate the functionality of a Flask application that simulates a Spotify Top Tracks App. The tests ensure that routes (home, logout, profile, top_tracks, top_artists, top_albums) behave as expected. For example, the test_home checks if the homepage displays the welcome message. The test_logout ensures the user is successfully logged out by removing the access token from the session. The remaining tests verify that the profile and various content routes return appropriate responses only when a valid access_token is present in the session. Each test uses Flask's test client and session_transaction to mock user sessions and simulate route access.
to run the tests, enter 'python -m unittest test_app.py' in to the console hwile in the folder.

WALK THROUGH
Visit the Initial Webpage:
Navigate to the homepage of the web application.

Sign In with Spotify:
Click the "Sign in with Spotify" button.
Enter your Spotify login credentials on the Spotify login page.
Upon successful login, you are redirected back to the application.

Profile Page:
View your Spotify-related data displayed on the profile page.
Use the navigation bar to explore other pages within the app.

Interact with Data:
On applicable pages, use buttons or controls to modify time frames (e.g., weekly, monthly, or yearly stats).

Log Out (Optional):
Click the log out button if you wish to end your session.

The base address of Web API is https://api.spotify.com.


TECH STACK
python flask html css





