from vnstock import Quote
import pandas as pd
import numpy as np
from fastapi import HTTPException, Query
from app.services.cache import cacheGet, cacheSet
from app.core.config import CACHE_TTL


# ============================
# Data Normalizer
# ============================

def normalize_data(data):

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

        records = df.to_dict(orient="records")

        if hasattr(data, 'name') and data.name:
            return {
                "name": data.name,
                "category": data.category if hasattr(data, 'category') else None,
                "data": records
            }

        return records

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


# ============================
# Quote Instance
# ============================

def get_quote(symbol: str, source: str):
    return Quote(symbol=symbol, source=source)


# ============================
# Service Functions
# ============================

def servicePriceHistory(
    symbol: str,
    source: str,
    start: str = None,
    end: str = None,
    length: str = None,
    interval: str = "1D"
):
    cacheKey = f"price:{source}:{symbol}:history:{start}:{end}:{length}:{interval}"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    quote = get_quote(symbol, source)

    if length:
        df = quote.history(length=length, interval=interval)
    elif start and end:
        df = quote.history(start=start, end=end, interval=interval)
    else:
        df = quote.history(length="1M", interval=interval)

    data = normalize_data(df)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def servicePriceIntraday(
    symbol: str,
    source: str,
    page_size: int = 100
):
    cacheKey = f"price:{source}:{symbol}:intraday:{page_size}"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    quote = get_quote(symbol, source)

    df = quote.intraday(page_size=page_size)

    data = normalize_data(df)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def servicePriceDepth(
    symbol: str,
    source: str
):
    if source.upper() == "KBS":
        raise HTTPException(
            status_code=400,
            detail="KBS does not support price_depth. Use VCI source instead."
        )

    cacheKey = f"price:{source}:{symbol}:depth"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    quote = get_quote(symbol, source)

    df = quote.price_depth()

    data = normalize_data(df)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


# ============================
# International Assets
# ============================

def serviceFxHistory(
    symbol: str,
    source: str = "MSN",
    start: str = None,
    end: str = None,
    interval: str = "1D"
):
    from vnstock import Vnstock

    cacheKey = f"fx:{source}:{symbol}:history:{start}:{end}:{interval}"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    fx = Vnstock().fx(symbol=symbol, source=source)

    if start and end:
        df = fx.quote.history(start=start, end=end)
    else:
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        df = fx.quote.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

    data = normalize_data(df)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def serviceCryptoHistory(
    symbol: str,
    source: str = "MSN",
    start: str = None,
    end: str = None,
    interval: str = "1D"
):
    from vnstock import Vnstock

    cacheKey = f"crypto:{source}:{symbol}:history:{start}:{end}:{interval}"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    crypto = Vnstock().crypto(symbol=symbol, source=source)

    if start and end:
        df = crypto.quote.history(start=start, end=end)
    else:
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        df = crypto.quote.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

    data = normalize_data(df)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def serviceWorldIndexHistory(
    symbol: str,
    source: str = "MSN",
    start: str = None,
    end: str = None,
    interval: str = "1D"
):
    from vnstock import Vnstock

    cacheKey = f"world_index:{source}:{symbol}:history:{start}:{end}:{interval}"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    index = Vnstock().world_index(symbol=symbol, source=source)

    if start and end:
        df = index.quote.history(start=start, end=end)
    else:
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        df = index.quote.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

    data = normalize_data(df)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data
