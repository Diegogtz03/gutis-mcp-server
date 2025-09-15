import os
from mcp.server.fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers
from mcp.server.auth.middleware.auth_context import get_access_token
from spotify.auth import getSpotifyUser
from spotify.tool import getCurrentPlayingTrack, tooglePlayPause, skipTrack, searchTrack, playTrack, addToQueue
from utils.headers import extract_token_from_header

from config import settings

mcp = FastMCP("Mosaic", stateless_http=True)

@mcp.tool(description="Greet a user by name with a welcome message from the MCP server")
def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to Mosaic, let Poke know your vibe!"

@mcp.tool(description="Get information about the MCP server including name, version, environment, and Python version")
def get_server_info() -> dict:
    return {
        "server_name": "Mosaic MCP Server by @sudoguti",
        "version": "1.0.0",
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "python_version": os.sys.version.split()[0]
    }

# Spotify Tools
@mcp.tool(description="Get the user's current playing track from Spotify")
def get_current_playing_track() -> dict:
    headers = get_http_headers()
    session = extract_token_from_header(headers)

    user = getSpotifyUser(session)

    if type(user) == str:
        return {"error": "User not authenticated with Spotify", "message": "Please direct the user to the following URL to authenticate: {}".format(user)}

    current_track = getCurrentPlayingTrack(session)

    if current_track is None:
        return {"error": "No track currently playing or unable to fetch track"}

    return {
        "track": current_track["item"]["name"],
        "artist": current_track["item"]["artists"][0]["name"],
        "currently_playing": current_track["is_playing"]
    }

@mcp.tool(description="Pause the user's current playing track on Spotify")
def pause_current_playing_track() -> dict:
    headers = get_http_headers()
    session = extract_token_from_header(headers)

    user = getSpotifyUser(session)

    if type(user) == str:
        return {"error": "User not authenticated with Spotify", "message": "Please direct the user to the following URL to authenticate: {}".format(user)}

    res = tooglePlayPause(session, play=False)

    if res.get("error"):
        return {"error": "Unable to pause playback"}

    return {"message": "Playback paused"}


@mcp.tool(description="Resume the user's current playing track on Spotify")
def resume_current_playing_track() -> dict:
    headers = get_http_headers()
    session = extract_token_from_header(headers)

    user = getSpotifyUser(session)

    if type(user) == str:
        return {"error": "User not authenticated with Spotify", "message": "Please direct the user to the following URL to authenticate: {}".format(user)}

    res = tooglePlayPause(session, play=True)

    if res.get("error"):
        return {"error": "Unable to resume playback"}

    return {"message": "Playback resumed"}


@mcp.tool(description="Skip back or forward the user's current playing track on Spotify")
def skip_current_playing_track(forward: bool) -> dict:
    headers = get_http_headers()
    session = extract_token_from_header(headers)

    user = getSpotifyUser(session)

    if type(user) == str:
        return {"error": "User not authenticated with Spotify", "message": "Please direct the user to the following URL to authenticate: {}".format(user)}

    res = skipTrack(session, forward=forward)

    if res.get("error"):
        return {"error": "Unable to skip track"}

    return {"message": "Track skipped {}".format("forward" if forward else "backward")}


@mcp.tool(description="Search for a track on Spotify by title and optionally artist and album")
def search_for_track(track_name: str, artist_name: str = "", album_name: str = "") -> dict:
    headers = get_http_headers()
    session = extract_token_from_header(headers)

    user = getSpotifyUser(session)

    if type(user) == str:
        return {"error": "User not authenticated with Spotify", "message": "Please direct the user to the following URL to authenticate: {}".format(user)}

    tracks = searchTrack(session, track_name, artist=artist_name, album=album_name)

    if tracks is None:
        return {"error": "No track found"}

    return tracks


@mcp.tool(description="Play a specific track on Spotify by its URI, needs search first")
def play_specific_track(track_uri: str) -> dict:
    headers = get_http_headers()
    session = extract_token_from_header(headers)

    user = getSpotifyUser(session)

    if type(user) == str:
        return {"error": "User not authenticated with Spotify", "message": "Please direct the user to the following URL to authenticate: {}".format(user)}

    res = playTrack(session, str(track_uri))

    if res.get("error"):
        return {"error": "Unable to play track"}

    return {"message": "Track is playing"}


@mcp.tool(description="Add a specific track to the user's Spotify queue by its URI, needs search first")
def add_track_to_queue(track_uri: str) -> dict:
    headers = get_http_headers()
    session = extract_token_from_header(headers)

    user = getSpotifyUser(session)

    if type(user) == str:
        return {"error": "User not authenticated with Spotify", "message": "Please direct the user to the following URL to authenticate: {}".format(user)}

    res = addToQueue(session, track_uri)

    if res.get("error"):
        return {"error": "Unable to add track to queue"}

    return {"message": "Track added to queue"}


# Letterbox Tools