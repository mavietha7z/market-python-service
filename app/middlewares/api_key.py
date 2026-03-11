from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import API_KEY

EXCLUDED_PATHS = {
    "/",
    "/docs",
    "/redoc",
    "/openapi.json"
}


class APIKeyMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return JSONResponse(
                status_code=401,
                content={
                    "status": 401,
                    "message": "Vui lòng cung cấp apikey"
                }
            )

        if api_key not in API_KEY:
            return JSONResponse(
                status_code=401,
                content={
                    "status": 401,
                    "message": "Apikey không hợp lệ"
                }
            )
        

        return await call_next(request)