from flask import Flask, g, redirect, request, session, url_for, render_template, jsonify
# g is the global object for temporary data
import requests
from dotenv import load_dotenv
import os # using os to get our env values from our env varibles

load_dotenv()
# Load environment variables
# Reads the .env file and loads the key-value pairs into the environment variables.
# Then we can then access these variables in your code using os.getenv()

# Spotify API credentials and URLs

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:5000/callback")


SCOPE = 'user-top-read user-read-recently-played playlist-read-private'
# SCOPE defines what kind of data and actions our app is allowed to acces from the users Spotify account and is displayed to the user before login.
# Debugging: Ensure credentials are loaded correctly
if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Missing Spotify API credentials! Check environment variables.")


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Cache for artist genres
artist_genre_cache = {}

# Spotify authorization URLs
AUTH_URL = f'https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}'

# url for redirect to spotifys login page
TOKEN_URL = 'https://accounts.spotify.com/api/token'
# where our app sends request to exhange the auth code for an acess token and rrefresh the tioken. The access token is used to auth API requests 


@app.before_request
def add_no_cache_headers():
    """This function is executed before every request. It checks if the requested endpoint is not 'static' (i.e., it doesn't apply to static files). It initializes a response variable in the `g` object, allowing the possibility to manipulate the response before sending it back to the client."""
    if request.endpoint != 'static':  # Don't apply to static files
        g.response = None  # Initialize response variable

@app.after_request
def add_cache_control_headers(response):
    """This function is executed after every request and modifies the response object before it is sent to the client. It adds headers to prevent caching by setting 'Cache-Control', 'Pragma', and 'Expires' to appropriate values."""
    # Prevent caching by adding these headers to all responses
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response



@app.route('/')
def home():
    """Main home page"""
    return render_template('home.html')
    # main home page where user can follow link to login

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/login')
def login():
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    return redirect(auth_url)
    # login route where we construct our auth url, flask uses redirect to send us to the spotify login page. User is prompted to login unless already loged in. 

@app.route('/callback')
def callback():
    """Callback route so spotify can send users to our website after Auth"""

    code = request.args.get('code')
    if not code:
        return redirect(url_for('home'))

    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=token_data)
    response_data = response.json()

    if response.status_code != 200:
        return f"Error: Unable to get token, {response.text}", 400

    session['access_token'] = response_data.get('access_token')
    return redirect(url_for('profile'))


@app.route('/logout')
def logout():
    """logout route"""
    session.pop('access_token', None)  # Remove access_token from session
    response = redirect(url_for('home'))  # Redirect to the home page
    return response



@app.route('/top/tracks', defaults={'time_range': None})
@app.route('/top/tracks/<time_range>')
def top_tracks(time_range):
    """Fetch user's top tracks based on the time range."""
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

    # If no time_range is provided, don't make an API call yet
    # Set default time_range if not provided
    if not time_range:
        time_range = 'short_term'  # Default to short_term if no time_range provided

    # Fetch top tracks from Spotify API
    headers = {'Authorization': f'Bearer {access_token}'}
    top_url = f'https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit=20'
    response = requests.get(top_url, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Unable to fetch data"}), response.status_code

    tracks_data = response.json()

    # Process and prepare data for rendering
    tracks = []
    for track in tracks_data['items']:
        tracks.append({
            'name': track['name'],
            'artist': ', '.join([artist['name'] for artist in track['artists']]),
            'album': track['album']['name'],
            'image': track['album']['images'][0]['url'] if track['album']['images'] else DEFAULT_IMAGE_URL,
            'preview_url': track['preview_url'],
            'spotify_url': track['external_urls']['spotify'] 
        })

    return render_template('top_tracks.html', tracks=tracks, time_range=time_range)



@app.route('/top/artists', defaults={'time_range': None})
@app.route('/top/artists/<time_range>')
def top_artists(time_range):
    """Fetch user's top artists based on the time range."""
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

    # If no time_range is provided, don't make an API call yet
    # Set default time_range if not provided
    if not time_range:
        time_range = 'short_term'  # Default to short_term if no time_range provided

    # Fetch top artists from Spotify API
    headers = {'Authorization': f'Bearer {access_token}'}
    top_url = f'https://api.spotify.com/v1/me/top/artists?time_range={time_range}&limit=20'
    response = requests.get(top_url, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Unable to fetch data"}), response.status_code

    artists_data = response.json()

    # Process and prepare data for rendering
    artists = []
    for artist in artists_data['items']:
        artists.append({
            'name': artist['name'],
            'image': artist['images'][0]['url'] if artist['images'] else '/static/default_image.png',
            'listeners': artist.get('popularity'),
            'spotify_url': artist['external_urls']['spotify'] 
        })

    return render_template('top_artists.html', artists=artists, time_range=time_range)



@app.route('/top/albums', defaults={'time_range': None})
@app.route('/top/albums/<time_range>')





def top_albums(time_range):
    """Fetch user's top albums based on the time range."""
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('home'))

    # If no time_range is provided, don't make an API call yet
    # Set default time_range if not provided
    if not time_range:
        time_range = 'short_term'  # Default to short_term if no time_range provided

    # If a time_range is provided, proceed with fetching data
    headers = {'Authorization': f'Bearer {access_token}'}
    top_url = f'https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit=20'
    response = requests.get(top_url, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Unable to fetch data"}), response.status_code

    tracks_data = response.json()

    # Extract album info from the top tracks
    albums = {}
    for track in tracks_data['items']:
        album_name = track['album']['name']
        album_id = track['album']['id']
        if album_name not in albums:
            albums[album_name] = {
                'id': album_id,
                'name': album_name,
                'image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'track_count': 0,
                'spotify_url': track['external_urls']['spotify'] 
            }
        albums[album_name]['track_count'] += 1

    # Sort albums by the number of top tracks
    sorted_albums = sorted(albums.values(), key=lambda x: x['track_count'], reverse=True)

    return render_template('top_albums.html', albums=sorted_albums, time_range=time_range)



@app.route('/profile')
def profile():
    """Fetch user profile from Spotify."""
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('home'))  # Redirect to home page if no access token

    headers = {'Authorization': f'Bearer {access_token}'}

    # Fetch user profile
    user_url = 'https://api.spotify.com/v1/me'
    response = requests.get(user_url, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Unable to fetch data"}), response.status_code

    user_data = response.json()

    # Extract basic user profile data
    profile_data = {
        'name': user_data['display_name'],
        'image': user_data['images'][0]['url'] if user_data['images'] else None
    }

    # Fetch user's playlists (now including images)
    playlists_url = 'https://api.spotify.com/v1/me/playlists?limit=50'
    playlists_response = requests.get(playlists_url, headers=headers)
    playlists = []
    if playlists_response.status_code == 200:
        playlists_data = playlists_response.json()
        playlists = [{'name': playlist['name'], 
                      'url': playlist['external_urls']['spotify'],
                      'image': playlist['images'][0]['url'] if playlist['images'] else None}
                     for playlist in playlists_data['items']]

    # Fetch user's top tracks 
    top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks?limit=10'
    top_tracks_response = requests.get(top_tracks_url, headers=headers)
    top_tracks = []
    if top_tracks_response.status_code == 200:
        top_tracks_data = top_tracks_response.json()
        top_tracks = [{'name': track['name'], 
                       'artist': track['artists'][0]['name'], 
                       'url': track['external_urls']['spotify'],
                       'album_cover': track['album']['images'][0]['url'] if track['album']['images'] else None} 
                      for track in top_tracks_data['items']]

    # Prepare all data for rendering
    profile_data['playlists'] = playlists
    profile_data['top_tracks'] = top_tracks

    return render_template('profile.html', profile=profile_data)


# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000) 

