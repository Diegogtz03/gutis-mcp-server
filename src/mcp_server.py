#!/usr/bin/env python3
import os
from mcp.server.fastmcp import FastMCP

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
def get_current_playing_track(user_email: str) -> dict:
    # Here you would implement the logic to interact with the Spotify API
    # and retrieve the current playing track for the given user_email.
    # This is just a placeholder implementation.
    print(f"Fetching current playing track for user_email: {user_email}")

    return {
        "user_email": user_email,
        "track": "Some Song",
        "artist": "Some Artist",
        "currently_playing": True
    }