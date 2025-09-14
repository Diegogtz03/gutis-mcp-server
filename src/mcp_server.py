#!/usr/bin/env python3
import os
from mcp.server.fastmcp import FastMCP
from mcp.server.auth.middleware.auth_context import get_access_token
from spotify.auth import getSpotifyUser
from spotify.tool import getCurrentPlayingTrack

from config import settings

mcp = FastMCP("Mosaic")

@mcp.tool(description="Greet a user by name with a welcome message from the MCP server")
def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to our Mosaic MCP server running on Heroku!"

@mcp.tool(description="Get information about the MCP server including name, version, environment, and Python version")
def get_server_info() -> dict:
    return {
        "server_name": "Mosaic MCP Server",
        "version": "1.0.0",
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "python_version": os.sys.version.split()[0]
    }

@mcp.tool(description="Get the users current playing track from Spotify with their unique email")
def get_current_playing_track() -> dict:
    user = getSpotifyUser("test_session")

    if type(user) == str:
        print("USER FROM DB: ", user)
        return {"error": "User not authenticated with Spotify", "message": "Please direct the user to the following URL to authenticate: {}".format(user)}

    print("USER FROM DB: ", user)
    current_track = getCurrentPlayingTrack()

    return {
        "user_email": user["email"],
        "track": current_track["name"],
        "artist": current_track["artists"][0]["name"],
        "currently_playing": True
    }