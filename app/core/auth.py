from fastapi import HTTPException
from app.core.config import API_KEYS


def verify_api_key(api_key: str):

    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )