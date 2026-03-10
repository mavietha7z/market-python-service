import os
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = os.getenv("API_KEY", "dev-key")

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)


def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key

    raise HTTPException(
        status_code=401,
        detail="Invalid API Key"
    )