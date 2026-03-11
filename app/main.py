import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Header, HTTPException
from cachetools import TTLCache

from app.routes.company import router as company_router
from app.core.auth import verify_api_key

from app.middlewares.api_key import APIKeyMiddleware
from app.routes.listing import router as listing_router




# ==============================
# FastAPI App
# ==============================

app = FastAPI(
    title="Market Python Service",
    version="1.0.0",
    description="Vietnam Stock Market Data API powered by vnstock"
)

app.add_middleware(APIKeyMiddleware)

# ==============================
# Cache RAM
# ==============================

cache = TTLCache(
    maxsize=1000,  # số request cache
    ttl=300        # 5 phút
)

# ==============================
# Supported Data Sources
# ==============================

VALID_SOURCES = {"KBS", "VCI"}

# ==============================
# Helper Functions
# ==============================

def validate_source(source: str) -> str:
    """
    Validate source parameter
    """
    source = source.upper()

    if source not in VALID_SOURCES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid source. Supported sources: {', '.join(VALID_SOURCES)}"
        )

    return source


def normalize_data(data):
    """
    Convert pandas DataFrame/Series → JSON serializable
    """
    import pandas as pd
    import numpy as np

    if data is None:
        return None

    if isinstance(data, pd.DataFrame):

        df = data.replace({
            np.nan: None,
            pd.NaT: None,
            np.inf: None,
            -np.inf: None
        })

        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].apply(
                    lambda x: x.isoformat() if x else None
                )

        return df.to_dict(orient="records")

    if isinstance(data, pd.Series):

        series = data.replace({
            np.nan: None,
            pd.NaT: None,
            np.inf: None,
            -np.inf: None
        })

        return series.to_dict()

    if isinstance(data, (dict, list)):
        return data

    return data


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

# ==============================
# System Endpoints
# ==============================

@app.get("/")
def root():
    return {
        "service": "Market Python Service",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health(api_key: str = Header(..., alias="X-API-Key")):
    verify_api_key(api_key)

    return {
        "status": "ok"
    }