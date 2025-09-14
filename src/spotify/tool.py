from .auth import getSpotifyUser, refreshAccessToken
from config import settings
import requests

def getCurrentPlayingTrack():
    user = getSpotifyUser("test_session")

    if not user:
        return None

    # fetch current playing track from Spotify API
    headers = {
        "Authorization": "Bearer {}".format(user["access_token"])
    }
    response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        new_token_data = refreshAccessToken(user["refresh_token"])
        
        if "access_token" in new_token_data:
            refreshAccessToken("test_session", new_token_data["access_token"])