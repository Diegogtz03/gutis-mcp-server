import contextlib
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth import AuthMiddleware
from config import settings
from mcp_server import mcp as mcp_router
import json

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp_router.session_manager.run():
        yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/.well-known/oauth-protected-resource/mcp")
async def oauth_protected_resource_metadata():
    """
    OAuth 2.0 Protected Resource Metadata endpoint for MCP client discovery.
    Required by the MCP specification for authorization server discovery.
    """

    response = json.loads(settings.METADATA_JSON_RESPONSE)
    return response

@app.get("/.well-known/oauth-protected-resource/resource")
async def oauth_protected_resource():
    """
    OAuth 2.0 Protected Resource endpoint for MCP client discovery.
    Required by the MCP specification for authorization server discovery.
    """

    response = json.loads(settings.METADATA_JSON_RESPONSE)
    return response

mcp_server = mcp_router.streamable_http_app()
app.add_middleware(AuthMiddleware)
app.mount("/", mcp_server)

def main():
    """Main entry point for the MCP server."""
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT, log_level="debug")

if __name__ == "__main__":
    main()