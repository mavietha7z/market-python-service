import vnstock
import numpy as np
import pandas as pd

from vnstock import Listing
from fastapi import HTTPException

from app.core.config import CACHE_TTL
from app.services.cache import cacheGet, cacheSet


# ============================
# Helpers
# ============================
def normalize_data(data):
    if data is None:
        return None

    if isinstance(data, pd.DataFrame):
        normalizedDataFrame = data.replace({
            np.nan: None,
            pd.NaT: None,
            np.inf: None,
            -np.inf: None
        })

        for columnName in normalizedDataFrame.columns:
            if pd.api.types.is_datetime64_any_dtype(normalizedDataFrame[columnName]):
                normalizedDataFrame[columnName] = normalizedDataFrame[columnName].apply(
                    lambda value: value.isoformat() if value is not None else None
                )

        return normalizedDataFrame.to_dict(orient="records")

    if isinstance(data, pd.Series):
        normalizedSeries = data.replace({
            np.nan: None,
            pd.NaT: None,
            np.inf: None,
            -np.inf: None
        })

        normalizedSeries = normalizedSeries.apply(
            lambda value: value.isoformat() if hasattr(value, "isoformat") and value is not None else value
        )

        return normalizedSeries.to_dict()

    if isinstance(data, (dict, list)):
        return data

    return data


def build_error(status_code: int, message: str):
    raise HTTPException(
        status_code=status_code,
        detail=message
    )


def normalize_source(source: str) -> str:
    normalizedSource = source.upper().strip()

    return normalizedSource


def normalize_exchange(exchange: str) -> str:
    return exchange.upper().strip()


def normalize_group(group: str) -> str:
    return group.strip()


def normalize_symbol(symbol: str) -> str:
    return symbol.upper().strip()


def get_cache_value(cache_key: str):
    cachedValue = cacheGet(cache_key)

    if cachedValue is not None:
        return cachedValue

    return None


def get_listing(source: str):
    normalizedSource = normalize_source(source)

    try:
        return Listing(source=normalizedSource)
    except Exception as error:
        build_error(
            500,
            f"Không thể khởi tạo Listing cho nguồn '{normalizedSource}': {str(error)}"
        )


def get_or_set_cache(cache_key: str, fetch_function):
    cachedValue = get_cache_value(cache_key)
    if cachedValue is not None:
        return cachedValue

    data = fetch_function()
    cacheSet(cache_key, data, CACHE_TTL)

    return data


def execute_listing_dataframe_method(source: str, cache_key: str, method_name: str, **kwargs):
    def fetch_data():
        listingInstance = get_listing(source)

        if not hasattr(listingInstance, method_name):
            build_error(
                400,
                f"Phương thức '{method_name}' không được hỗ trợ cho nguồn '{source}'"
            )

        methodObject = getattr(listingInstance, method_name)
        rawData = methodObject(**kwargs)
        return normalize_data(rawData)

    return get_or_set_cache(cache_key, fetch_data)


# ============================
# Service Functions
# ============================
def service_listing_all_symbols(source: str):
    normalizedSource = normalize_source(source)
    cacheKey = f"listing:{normalizedSource}:all_symbols"

    return execute_listing_dataframe_method(
        source=normalizedSource,
        cache_key=cacheKey,
        method_name="all_symbols"
    )


def service_listing_symbols_by_exchange(source: str, exchange: str):
    normalizedSource = normalize_source(source)
    normalizedExchange = normalize_exchange(exchange)
    cacheKey = f"listing:{normalizedSource}:exchange:{normalizedExchange}"

    return execute_listing_dataframe_method(
        source=normalizedSource,
        cache_key=cacheKey,
        method_name="symbols_by_exchange",
        exchange=normalizedExchange
    )


def service_listing_symbols_by_group(source: str, group: str):
    normalizedSource = normalize_source(source)
    normalizedGroup = normalize_group(group)
    cacheKey = f"listing:{normalizedSource}:group:{normalizedGroup}"

    return execute_listing_dataframe_method(
        source=normalizedSource,
        cache_key=cacheKey,
        method_name="symbols_by_group",
        group_name=normalizedGroup
    )


def service_listing_symbols_by_industries(source: str):
    normalizedSource = normalize_source(source)
    cacheKey = f"listing:{normalizedSource}:symbols_by_industries"

    return execute_listing_dataframe_method(
        source=normalizedSource,
        cache_key=cacheKey,
        method_name="symbols_by_industries"
    )


def service_listing_industries_icb(source: str):
    normalizedSource = normalize_source(source)

    if normalizedSource == "KBS":
        build_error(
            400,
            "KBS không hỗ trợ industries_icb. Hãy dùng symbols_by_industries()."
        )

    cacheKey = f"listing:{normalizedSource}:industries_icb"

    return execute_listing_dataframe_method(
        source=normalizedSource,
        cache_key=cacheKey,
        method_name="industries_icb"
    )


def service_listing_all_indices(source: str):
    normalizedSource = normalize_source(source)
    cacheKey = f"listing:{normalizedSource}:all_indices"

    def fetch_data():
        return list(vnstock.INDICES_MAP.keys())

    return get_or_set_cache(cacheKey, fetch_data)


def service_listing_indices_by_group(source: str, group: str):
    normalizedSource = normalize_source(source)
    normalizedGroup = normalize_group(group)
    cacheKey = f"listing:{normalizedSource}:indices_by_group:{normalizedGroup}"

    def fetch_data():
        if normalizedGroup not in vnstock.INDEX_GROUPS:
            build_error(
                400,
                f"Nhóm chỉ số không hợp lệ. Các nhóm được hỗ trợ: {', '.join(vnstock.INDEX_GROUPS.keys())}"
            )

        return list(vnstock.INDEX_GROUPS[normalizedGroup])

    return get_or_set_cache(cacheKey, fetch_data)


def service_listing_search_symbol_id(source: str, symbol: str):
    normalizedSource = normalize_source(source)
    normalizedSymbol = normalize_symbol(symbol)
    cacheKey = f"listing:{normalizedSource}:search_symbol_id:{normalizedSymbol}"

    def fetch_data():
        try:
            from vnstock.explorer.msn.listing import Listing as MsnListing

            listingInstance = MsnListing()
            rawData = listingInstance.search_symbol_id(normalizedSymbol)

            return normalize_data(rawData)
        except Exception as error:
            build_error(
                500,
                f"Lỗi khi tìm mã quốc tế '{normalizedSymbol}': {str(error)}"
            )

    return get_or_set_cache(cacheKey, fetch_data)