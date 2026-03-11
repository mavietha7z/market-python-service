from dotenv import load_dotenv

load_dotenv()

from cachetools import TTLCache
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, HTTPException
from app.middlewares.api_key import APIKeyMiddleware
from fastapi.exceptions import RequestValidationError

from app.routes.price import router as price_router
from app.routes.listing import router as listing_router
from app.routes.company import router as company_router

# ==============================
# FastAPI App
# ==============================
app = FastAPI(
    version="1.0.0",
    title="API Chứng khoán Việt Nam - vnstock",
    description="API cung cấp dữ liệu chứng khoán Việt Nam từ các nguồn như KBS, VCI. Hỗ trợ dữ liệu lịch sử, giá intraday, độ sâu thị trường, tin tức công ty, sự kiện và nhiều hơn nữa."
)

# ==============================
# Exception Handlers
# ==============================
@app.exception_handler(HTTPException)
async def global_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "message": exc.detail
        }
    )


@app.exception_handler(RequestValidationError)
async def global_validation_exception_handler(request: Request, exc: RequestValidationError):
    firstError = exc.errors()[0] if exc.errors() else None

    if firstError:
        errorLocation = " -> ".join(str(item) for item in firstError.get("loc", []))
        errorMessage = firstError.get("msg", "Dữ liệu gửi lên không hợp lệ")
        finalMessage = f"{errorLocation}: {errorMessage}"
    else:
        finalMessage = "Dữ liệu gửi lên không hợp lệ"

    return JSONResponse(
        status_code=422,
        content={
            "status": 422,
            "message": finalMessage
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": 500,
            "message": "Internal server error"
        }
    )

# ==============================
# Cache RAM
# ==============================
cache = TTLCache(
    maxsize=1000,  # số request cache
    ttl=300        # 5 phút
)

# ==============================
# System Endpoints
# ==============================
@app.get("/")
def root():
    return {
        "status": 200,
        "message": "running",
        "version": "1.0.0",
        "service": "API Chứng khoán Việt Nam - vnstock"
    }

# ==============================
# Middleware
# ==============================
app.add_middleware(APIKeyMiddleware)

# ==============================
# Routers
# ==============================
app.include_router(
    company_router,
    prefix="/api/v1/company",
    tags=["Company"]
)

app.include_router(
    listing_router,
    prefix="/api/v1/listing",
    tags=["Listing"]
)

app.include_router(
    price_router,
    prefix="/api/v1/price",
    tags=["Price"]
)