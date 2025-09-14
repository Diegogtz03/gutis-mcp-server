import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SCALEKIT_ENVIRONMENT_URL: str = os.environ.get("SCALEKIT_ENVIRONMENT_URL", "")
    SCALEKIT_CLIENT_ID: str = os.environ.get("SCALEKIT_CLIENT_ID", "")
    SCALEKIT_CLIENT_SECRET: str = os.environ.get("SCALEKIT_CLIENT_SECRET", "")
    SCALEKIT_RESOURCE_METADATA_URL: str = os.environ.get("SCALEKIT_RESOURCE_METADATA_URL", "")
    SCALEKIT_AUDIENCE_NAME: str = os.environ.get("SCALEKIT_AUDIENCE_NAME", "")
    
    SPOTIFY_CLIENT_ID: str = os.environ.get("SPOTIFY_CLIENT_ID", "")
    SPOTIFY_CLIENT_SECRET: str = os.environ.get("SPOTIFY_CLIENT_SECRET", "")
    SPOTIFY_REDIRECT_URI: str = os.environ.get("SPOTIFY_REDIRECT_URI", "http://localhost:10000/callback")
    SPOTIFY_SCOPE: str = os.environ.get("SPOTIFY_SCOPE", "user-read-playback-state")
    DB_CONNECTION_STRING: str = os.environ.get("DB_CONNECTION_STRING", "")
    METADATA_JSON_RESPONSE: str = os.environ.get("METADATA_JSON_RESPONSE", "")


    # Server Port
    PORT: int = int(os.environ.get("PORT", 10000))

    def __post_init__(self):
        if not self.SPOTIFY_CLIENT_ID:
            raise ValueError("SPOTIFY_CLIENT_ID environment variable not set")
        if not self.SPOTIFY_CLIENT_SECRET:
            raise ValueError("SPOTIFY_CLIENT_SECRET environment variable not set")
        if not self.SPOTIFY_SCOPE:
            raise ValueError("SPOTIFY_SCOPE environment variable not set")
        if not self.SPOTIFY_REDIRECT_URI:
            raise ValueError("SPOTIFY_REDIRECT_URI environment variable not set")
        if not self.SCALEKIT_CLIENT_ID:
            raise ValueError("SCALEKIT_CLIENT_ID environment variable not set")
        if not self.SCALEKIT_CLIENT_SECRET:
            raise ValueError("SCALEKIT_CLIENT_SECRET environment variable not set")
        if not self.SCALEKIT_ENVIRONMENT_URL:
            raise ValueError("SCALEKIT_ENVIRONMENT_URL environment variable not set")
        if not self.SCALEKIT_RESOURCE_METADATA_URL:
            raise ValueError("SCALEKIT_RESOURCE_METADATA_URL environment variable not set")
        if not self.SCALEKIT_AUDIENCE_NAME:
            raise ValueError("SCALEKIT_AUDIENCE_NAME environment variable not set")
        if not self.DB_CONNECTION_STRING:
            raise ValueError("DB_CONNECTION_STRING environment variable not set")

settings = Settings()