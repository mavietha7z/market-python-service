import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Query, HTTPException, Header
from pydantic import BaseModel
from vnstock import Vnstock
from cachetools import TTLCache
from app.routes.company import router as companyRouter
from app.core.auth import verify_api_key

app = FastAPI(
    title="Market Python Service",
    version="1.0.0"
)

# Cache RAM
# maxsize = số request cache
# ttl = 300s = 5 phút
cache = TTLCache(maxsize=1000, ttl=300)

# Các nguồn dữ liệu được hỗ trợ
VALID_SOURCES = ["KBS", "VCI"]


def normalize_data(data):
    """Chuẩn hóa dữ liệu từ pandas DataFrame/Series thành JSON"""
    import pandas as pd
    import numpy as np

    if data is None:
        return None

    if isinstance(data, pd.DataFrame):
        df = data.replace({np.nan: None, pd.NaT: None, np.inf: None, -np.inf: None})
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].apply(lambda x: x.isoformat() if x is not None else None)
        return df.to_dict(orient="records")

    if isinstance(data, pd.Series):
        series = data.replace({np.nan: None, pd.NaT: None, np.inf: None, -np.inf: None})
        if pd.api.types.is_datetime64_any_dtype(series):
            series = series.apply(lambda x: x.isoformat() if x is not None else None)
        return series.to_dict()

    if isinstance(data, (dict, list)):
        return data

    return data


def validate_source(source: str) -> str:
    """Validate source parameter"""
    if source not in VALID_SOURCES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid source. Supported sources: {', '.join(VALID_SOURCES)}"
        )
    return source


app.include_router(companyRouter)


@app.get("/")
def root():
    return {
        "message": "Python market service is running"
    }


@app.get("/health")
def health(api_key: str = Header(..., alias="X-API-Key")):
    verify_api_key(api_key)

    return {
        "status": "ok"
    }

