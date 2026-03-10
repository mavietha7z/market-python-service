import os
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = os.getenv("API_KEY", "dev-key")

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)


def verify_api_key(api_key: str = Security(api_key_header)):
    # Đọc API_KEY trong function để đảm bảo load_dotenv() đã chạy
    valid_api_key = os.getenv("API_KEY", "dev-key")
    
    if api_key == valid_api_key:
        return api_key

    raise HTTPException(
        status_code=401,
        detail="Invalid API Key"
    )