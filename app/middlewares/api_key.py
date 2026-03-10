from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.auth import verify_api_key


class APIKeyMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # Bỏ qua docs
        if request.url.path in [
            "/docs",
            "/openapi.json",
            "/redoc",
            "/"
        ]:
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")

        if not api_key:
            raise HTTPException(
                status_code=401,
                detail="Missing API Key"
            )

        verify_api_key(api_key)

        response = await call_next(request)

        return response