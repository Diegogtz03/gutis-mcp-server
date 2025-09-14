from .auth import getSpotifyUser, refreshAccessToken
from config import settings
import requests

def getCurrentPlayingTrack():
    user = getSpotifyUser("test_session")

    if type(user) == str:
        return None

    # fetch current playing track from Spotify API
    headers = {
        "Authorization": "Bearer {}".format(user[2])
    }

    response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("Access token expired, refreshing...")
        new_token_data = refreshAccessToken(user[3])

    return response.json()