from .auth import getSpotifyUser, refreshAccessToken
from config import settings
import requests
from utils.hash import unencryptToken
from db import updateSpotifyAccessToken

def getCurrentPlayingTrack(session):
    user = getSpotifyUser(session)

    if type(user) == str:
        return None

    headers = {
        "Authorization": "Bearer {}".format(unencryptToken(user[2]))
    }

    response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        new_token_data = refreshAccessToken(unencryptToken(user[3]))
        updateSpotifyAccessToken(session, new_token_data["access_token"])

        # retry the request with the new access token
        headers["Authorization"] = "Bearer {}".format(new_token_data["access_token"])
        response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def tooglePlayPause(session, play=True):
    user = getSpotifyUser(session)

    if type(user) == str:
        return None

    headers = {
        "Authorization": "Bearer {}".format(unencryptToken(user[2]))
    }

    response = requests.put("https://api.spotify.com/v1/me/player/pause" if not play else "https://api.spotify.com/v1/me/player/play", headers=headers)

    if response.status_code == 200:
        return {"message": "Playback {}".format("paused" if play else "resumed")}
    elif response.status_code == 401:
        new_token_data = refreshAccessToken(unencryptToken(user[3]))
        updateSpotifyAccessToken(session, new_token_data["access_token"])

        # retry the request with the new access token
        headers["Authorization"] = "Bearer {}".format(new_token_data["access_token"])
        response = requests.put("https://api.spotify.com/v1/me/player/pause" if play else "https://api.spotify.com/v1/me/player/play", headers=headers)

        if response.status_code == 200:
            return {"message": "Playback {}".format("paused" if play else "resumed")}
        else:
            return {"error": "Unable to {}".format("pause" if play else "resume")}
    else:
        return {"error": "Unable to {}".format("pause" if play else "resume")}


def skipTrack(session, forward=True):
    user = getSpotifyUser(session)

    if type(user) == str:
        return None

    headers = {
        "Authorization": "Bearer {}".format(unencryptToken(user[2]))
    }

    response = requests.post("https://api.spotify.com/v1/me/player/{}".format("next" if forward else "previous"), headers=headers)

    if response.status_code == 200:
        return {"message": "Skipped {}".format("forward" if forward else "backward")}
    elif response.status_code == 401:
        new_token_data = refreshAccessToken(unencryptToken(user[3]))
        updateSpotifyAccessToken(session, new_token_data["access_token"])

        # retry the request with the new access token
        headers["Authorization"] = "Bearer {}".format(new_token_data["access_token"])
        response = requests.post("https://api.spotify.com/v1/me/player/{}".format("next" if forward else "previous"), headers=headers)

        if response.status_code == 200:
            return {"message": "Skipped {}".format("forward" if forward else "backward")}
    else:
        return {"error": "Unable to skip {}".format("forward" if forward else "backward")}


def searchTrack(session, title, artist="", album=""):
    user = getSpotifyUser(session)

    if type(user) == str:
        return None

    headers = {
        "Authorization": "Bearer {}".format(unencryptToken(user[2]))
    }

    query = title

    if artist != "":
        query += f" artist:{artist}"
    if album != "":
        query += f" album:{album}"
    
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params={"q": query, "type": "track", "limit": 5})

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        new_token_data = refreshAccessToken(unencryptToken(user[3]))
        updateSpotifyAccessToken(session, new_token_data["access_token"])

        # retry the request with the new access token
        headers["Authorization"] = "Bearer {}".format(new_token_data["access_token"])
        response = requests.get("https://api.spotify.com/v1/search", headers=headers, params={"q": query, "type": "track"})

    if response.status_code == 200:
        return response.json()
    else:
        return None

def playTrack(session, track_uri):
    user = getSpotifyUser(session)

    if type(user) == str:
        return None

    headers = {
        "Authorization": "Bearer {}".format(unencryptToken(user[2]))
    }

    response = requests.put("https://api.spotify.com/v1/me/player/play", headers=headers, json={"uris": [track_uri]})

    if response.status_code == 200:
        return {"message": "Playback started"}
    elif response.status_code == 401:
        new_token_data = refreshAccessToken(unencryptToken(user[3]))
        updateSpotifyAccessToken(session, new_token_data["access_token"])

        # retry the request with the new access token
        headers["Authorization"] = "Bearer {}".format(new_token_data["access_token"])
        response = requests.put("https://api.spotify.com/v1/me/player/play", headers=headers, json={"uris": [track_uri]})

        if response.status_code == 200:
            return {"message": "Playback started"}
    else:
        return {"error": "Unable to start playback"}


def addToQueue(session, track_uri):
    user = getSpotifyUser(session)

    if type(user) == str:
        return None

    headers = {
        "Authorization": "Bearer {}".format(unencryptToken(user[2]))
    }

    response = requests.post("https://api.spotify.com/v1/me/player/queue", headers=headers, params={"uri": track_uri})

    if response.status_code == 200:
        return {"message": "Track added to queue"}
    elif response.status_code == 401:
        new_token_data = refreshAccessToken(unencryptToken(user[3]))
        updateSpotifyAccessToken(session, new_token_data["access_token"])

        # retry the request with the new access token
        headers["Authorization"] = "Bearer {}".format(new_token_data["access_token"])
        response = requests.post("https://api.spotify.com/v1/me/player/queue", headers=headers, params={"uri": track_uri})

        if response.status_code == 200:
            return {"message": "Track added to queue"}
    else:
        return {"error": "Unable to add track to queue"}