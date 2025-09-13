#!/usr/bin/env python3
import os
from fastmcp import FastMCP

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

@mcp.tool(description="Get the users current playing track from Spotify with their user ID")
def get_current_playing_track(user_id: str) -> dict:
    # Here you would implement the logic to interact with the Spotify API
    # and retrieve the current playing track for the given user_id.
    # This is just a placeholder implementation.
    print(f"Fetching current playing track for user_id: {user_id}")

    return {
        "user_id": user_id,
        "track": "Some Song",
        "artist": "Some Artist",
        "currently_playing": True
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"Starting FastMCP server on {host}:{port}")
    
    mcp.run(
        transport="http",
        host=host,
        port=port
    )
