import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = 'c8beb3fb30c6460387f017117462bbec'
SPOTIPY_CLIENT_SECRET = 'd5297c9cedac4564861c017063a2c1f7'
SPOTIPY_REDIRECT_URI = 'http://localhost:3001/callback/'

scope = "user-library-read user-top-read playlist-modify-private"

sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                        client_secret=SPOTIPY_CLIENT_SECRET,
                        redirect_uri=SPOTIPY_REDIRECT_URI,
                        scope=scope)

def get_spotify_client():
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print(f"Please navigate to this URL and authorize the app: {auth_url}")
        response = input("Enter the full URL you were redirected to: ")
        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)
    else:
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp
