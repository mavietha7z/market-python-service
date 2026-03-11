from vnstock import Listing
import pandas as pd
import numpy as np
from fastapi import HTTPException
from app.core.cache import cache
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


# ============================
# VNStock Instance
# ============================

def get_listing(source: str):
    return Listing(source=source)


# ============================
# Service Functions
# ============================

def serviceListingAllSymbols(source: str):

    cacheKey = f"listing:{source}:all_symbols"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    listing = get_listing(source)

    df = listing.all_symbols()

    data = normalize_data(df)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def serviceListingSymbolsByExchange(source: str, exchange: str):

    cacheKey = f"listing:{source}:exchange:{exchange}"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    listing = get_listing(source)

    df = listing.symbols_by_exchange(exchange=exchange)

    data = normalize_data(df)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def serviceListingSymbolsByGroup(source: str, group: str):

    cacheKey = f"listing:{source}:group:{group}"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    listing = get_listing(source)

    series = listing.symbols_by_group(group_name=group)

    data = normalize_data(series)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def serviceListingSymbolsByIndustries(source: str):

    cacheKey = f"listing:{source}:industries"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    listing = get_listing(source)

    df = listing.symbols_by_industries()

    data = normalize_data(df)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def serviceListingIndustriesICB(source: str):
    if source.upper() == "KBS":
        raise HTTPException(
            status_code=400,
            detail="KBS does not support ICB classification. Use symbols_by_industries() instead."
        )

    cacheKey = f"listing:{source}:industries_icb"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    listing = get_listing(source)

    df = listing.industries_icb()

    data = normalize_data(df)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def serviceListingAllIndices(source: str):
    import vnstock

    cacheKey = f"listing:{source}:indices"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    data = list(vnstock.INDICES_MAP.keys())

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def serviceListingIndicesByGroup(source: str, group: str):
    import vnstock

    cacheKey = f"listing:{source}:indices_by_group:{group}"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    if group not in vnstock.INDEX_GROUPS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid group. Available groups: {', '.join(vnstock.INDEX_GROUPS.keys())}"
        )

    data = list(vnstock.INDEX_GROUPS[group])

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def serviceListingAllIndices(source: str):
    import vnstock

    cacheKey = f"listing:{source}:indices"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    data = list(vnstock.INDICES_MAP.keys())

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def serviceListingAllFutureIndices(source: str):

    cacheKey = f"listing:{source}:future_indices"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    listing = get_listing(source)

    series = listing.all_future_indices()

    data = normalize_data(series)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def serviceListingAllCoveredWarrant(source: str):

    cacheKey = f"listing:{source}:covered_warrant"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    listing = get_listing(source)

    series = listing.all_covered_warrant()

    data = normalize_data(series)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def serviceListingAllBonds(source: str):

    cacheKey = f"listing:{source}:bonds"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    listing = get_listing(source)

    series = listing.all_bonds()

    data = normalize_data(series)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def serviceListingAllGovernmentBonds(source: str):
    if source.upper() == "KBS":
        raise HTTPException(
            status_code=400,
            detail="KBS does not support government bonds. Use VCI source instead."
        )

    cacheKey = f"listing:{source}:government_bonds"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    listing = get_listing(source)

    series = listing.all_government_bonds()

    data = normalize_data(series)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data


def serviceListingSearchSymbolId(symbol: str):
    from vnstock.explorer.msn.listing import Listing as MsnListing

    cacheKey = f"listing:search_symbol_id:{symbol}"

    cached = cacheGet(cacheKey)
    if cached:
        return cached

    listing = MsnListing()

    df = listing.search_symbol_id(symbol)

    data = normalize_data(df)

    cacheSet(cacheKey, data, CACHE_TTL)

    return data