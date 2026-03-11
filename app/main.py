from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from cachetools import TTLCache
from app.middlewares.api_key import APIKeyMiddleware

from app.routes.price import router as price_router
from app.routes.listing import router as listing_router
from app.routes.company import router as company_router
from app.routes.listing import router as listing_router

# ==============================
# FastAPI App
# ==============================
app = FastAPI(
    version="1.0.0",
    title="API Chứng khoán Việt Nam - vnstock",
    description="API cung cấp dữ liệu chứng khoán Việt Nam từ các nguồn như KBS, VCI. Hỗ trợ dữ liệu lịch sử, giá intraday, độ sâu thị trường, tin tức công ty, sự kiện và nhiều hơn nữa."
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
        "version": "1.0.0",
        "status": "running",
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