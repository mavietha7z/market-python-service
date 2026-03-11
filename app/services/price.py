from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from fastapi import HTTPException
from vnstock import Quote, Vnstock

from app.core.config import CACHE_TTL
from app.services.cache import cacheGet, cacheSet


# ============================
# Constants
# ============================
SUPPORTED_SOURCES = {"KBS", "VCI"}
DEFAULT_HISTORY_LOOKBACK_DAYS = 30


# ============================
# Data Normalizer
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

        records = normalizedDataFrame.to_dict(orient="records")

        if hasattr(data, "name") and getattr(data, "name", None):
            return {
                "name": data.name,
                "category": getattr(data, "category", None),
                "data": records
            }

        return records

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


# ============================
# Error Helpers
# ============================
def raise_http_error(status_code: int, message: str):
    raise HTTPException(
        status_code=status_code,
        detail=message
    )


# ============================
# Normalizers
# ============================
def normalize_source(source: str) -> str:
    normalizedSource = source.upper().strip()

    if normalizedSource not in SUPPORTED_SOURCES:
        raise_http_error(
            400,
            "Nguồn không hợp lệ. Các nguồn được hỗ trợ: KBS, VCI"
        )

    return normalizedSource


def normalize_symbol(symbol: str) -> str:
    return symbol.upper().strip()


def normalize_interval(interval: str) -> str:
    return interval.strip()


# ============================
# Cache Helpers
# ============================
def get_cache_value(cache_key: str):
    cachedValue = cacheGet(cache_key)

    if cachedValue is not None:
        return cachedValue

    return None


def get_or_set_cache(cache_key: str, fetch_function):
    cachedValue = get_cache_value(cache_key)
    if cachedValue is not None:
        return cachedValue

    data = fetch_function()
    cacheSet(cache_key, data, CACHE_TTL)

    return data


# ============================
# Quote / Date Helpers
# ============================
def get_quote(symbol: str, source: str):
    normalizedSymbol = normalize_symbol(symbol)
    normalizedSource = normalize_source(source)

    try:
        return Quote(symbol=normalizedSymbol, source=normalizedSource)
    except Exception as error:
        raise_http_error(
            500,
            f"Không thể khởi tạo Quote cho mã '{normalizedSymbol}' với nguồn '{normalizedSource}': {str(error)}"
        )


def get_default_date_range():
    endDate = datetime.now()
    startDate = endDate - timedelta(days=DEFAULT_HISTORY_LOOKBACK_DAYS)

    return (
        startDate.strftime("%Y-%m-%d"),
        endDate.strftime("%Y-%m-%d")
    )


def resolve_history_date_range(start: str | None, end: str | None):
    if start and end:
        return start, end

    return get_default_date_range()


def build_history_cache_key(asset_type: str, source: str, symbol: str, start: str, end: str, interval: str):
    return f"{asset_type}:{source}:{symbol}:history:{start}:{end}:{interval}"


# ============================
# Stock Price Services
# ============================
def service_price_stock_history(
    symbol: str,
    source: str,
    start: str,
    end: str,
    interval: str
):
    normalizedSymbol = normalize_symbol(symbol)
    normalizedSource = normalize_source(source)
    normalizedInterval = normalize_interval(interval)

    cacheKey = build_history_cache_key(
        asset_type="price",
        source=normalizedSource,
        symbol=normalizedSymbol,
        start=start,
        end=end,
        interval=normalizedInterval
    )

    def fetch_data():
        quoteInstance = get_quote(normalizedSymbol, normalizedSource)

        try:
            rawData = quoteInstance.history(
                start=start,
                end=end,
                interval=normalizedInterval
            )
            return normalize_data(rawData)
        except Exception as error:
            raise_http_error(
                500,
                f"Lỗi khi lấy lịch sử giá cho mã '{normalizedSymbol}': {str(error)}"
            )

    return get_or_set_cache(cacheKey, fetch_data)


def service_price_stock_intraday(
    symbol: str,
    source: str,
    page_size: int = 100,
    get_all: bool = False,
    last_time: str | None = None,
    last_time_format: str = "iso"
):
    normalizedSymbol = normalize_symbol(symbol)
    normalizedSource = normalize_source(source)
    normalizedLastTimeFormat = last_time_format.strip().lower()

    cacheKey = (
        f"price:{normalizedSource}:{normalizedSymbol}:intraday:"
        f"{page_size}:{get_all}:{last_time}:{normalizedLastTimeFormat}"
    )

    def fetch_data():
        quoteInstance = get_quote(normalizedSymbol, normalizedSource)

        try:
            rawData = quoteInstance.intraday(
                page_size=page_size,
                get_all=get_all,
                last_time=last_time,
                last_time_format=normalizedLastTimeFormat
            )
            return normalize_data(rawData)
        except TypeError:
            # fallback nếu phiên bản vnstock hiện tại không hỗ trợ đầy đủ các tham số mới
            try:
                rawData = quoteInstance.intraday(page_size=page_size)
                return normalize_data(rawData)
            except Exception as error:
                raise_http_error(
                    500,
                    f"Lỗi khi lấy dữ liệu intraday cho mã '{normalizedSymbol}': {str(error)}"
                )
        except Exception as error:
            raise_http_error(
                500,
                f"Lỗi khi lấy dữ liệu intraday cho mã '{normalizedSymbol}': {str(error)}"
            )

    return get_or_set_cache(cacheKey, fetch_data)


# ============================
# International Asset Helpers
# ============================
def fetch_external_history_data(
    asset_name: str,
    asset_factory,
    symbol: str,
    source: str,
    start: str | None,
    end: str | None,
    interval: str
):
    normalizedSymbol = normalize_symbol(symbol)
    normalizedSource = normalize_source(source)
    normalizedInterval = normalize_interval(interval)
    resolvedStart, resolvedEnd = resolve_history_date_range(start, end)

    cacheKey = build_history_cache_key(
        asset_type=asset_name,
        source=normalizedSource,
        symbol=normalizedSymbol,
        start=resolvedStart,
        end=resolvedEnd,
        interval=normalizedInterval
    )

    def fetch_data():
        try:
            assetInstance = asset_factory(normalizedSymbol, normalizedSource)

            rawData = assetInstance.quote.history(
                start=resolvedStart,
                end=resolvedEnd,
                interval=normalizedInterval
            )

            return normalize_data(rawData)
        except TypeError:
            # fallback nếu quote.history không hỗ trợ interval ở asset đó
            try:
                assetInstance = asset_factory(normalizedSymbol, normalizedSource)

                rawData = assetInstance.quote.history(
                    start=resolvedStart,
                    end=resolvedEnd
                )

                return normalize_data(rawData)
            except Exception as error:
                raise_http_error(
                    500,
                    f"Lỗi khi lấy dữ liệu {asset_name} cho mã '{normalizedSymbol}': {str(error)}"
                )
        except Exception as error:
            raise_http_error(
                500,
                f"Lỗi khi lấy dữ liệu {asset_name} cho mã '{normalizedSymbol}': {str(error)}"
            )

    return get_or_set_cache(cacheKey, fetch_data)


# ============================
# International Asset Services
# ============================
def service_price_fx_history(
    symbol: str,
    source: str,
    start: str,
    end: str,
    interval: str
):
    return fetch_external_history_data(
        asset_name="fx",
        asset_factory=lambda normalizedSymbol, normalizedSource: Vnstock().fx(
            symbol=normalizedSymbol,
            source=normalizedSource
        ),
        symbol=symbol,
        source=source,
        start=start,
        end=end,
        interval=interval
    )


def service_price_crypto_history(
    symbol: str,
    source: str,
    start: str,
    end: str,
    interval: str
):
    return fetch_external_history_data(
        asset_name="crypto",
        asset_factory=lambda normalizedSymbol, normalizedSource: Vnstock().crypto(
            symbol=normalizedSymbol,
            source=normalizedSource
        ),
        symbol=symbol,
        source=source,
        start=start,
        end=end,
        interval=interval
    )


def service_price_world_index_history(
    symbol: str,
    source: str,
    start: str,
    end: str,
    interval: str
):
    return fetch_external_history_data(
        asset_name="world_index",
        asset_factory=lambda normalizedSymbol, normalizedSource: Vnstock().world_index(
            symbol=normalizedSymbol,
            source=normalizedSource
        ),
        symbol=symbol,
        source=source,
        start=start,
        end=end,
        interval=interval
    )