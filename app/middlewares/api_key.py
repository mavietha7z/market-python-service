from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import os

API_KEY = os.getenv("API_KEY", "dev-key")


class ApiKeyMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # bỏ qua swagger
        if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)

        key = request.headers.get("X-API-Key")

        if key != API_KEY:
            from fastapi.responses import JSONResponse

            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid API Key"}
            )

        return await call_next(request)