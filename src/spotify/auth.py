from db import checkSpotifyExistingUser
from config import settings

def getSpotifyUser(session):
    user = checkSpotifyExistingUser(session)

    if not user:
        return "https://accounts.spotify.com/authorize?client_id={}&redirect_uri={}&response_type=code&scope={}&state={}".format(
            settings.SPOTIFY_CLIENT_ID,
            settings.SPOTIFY_REDIRECT_URI,
            settings.SPOTIFY_SCOPE,
            session
        )
    else:
        return user

def exchangeCodeForToken(code):
    import requests
    import base64

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI
    }

    response = requests.post(url, headers=headers, data=data)

    return response.json()

def refreshAccessToken(refresh_token):
    import requests
    import base64

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(url, headers=headers, data=data)
    
    return response.json()