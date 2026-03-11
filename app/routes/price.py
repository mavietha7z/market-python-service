from fastapi import APIRouter, Query, Header, HTTPException

from app.services.price import (
    servicePriceHistory,
    servicePriceIntraday,
    servicePriceDepth,
    serviceFxHistory,
    serviceCryptoHistory,
    serviceWorldIndexHistory
)

VALID_SOURCES = {"KBS", "VCI"}

router = APIRouter(
    prefix="",
    tags=["Price"]
)


# =============================
# Helpers
# =============================

def validate_source(source: str) -> str:
    source = source.upper()

    if source not in VALID_SOURCES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid source. Supported sources: {', '.join(VALID_SOURCES)}"
        )

    return source


def base_response(source: str, data, symbol: str = None):
    response = {
        "status": "success",
        "source": source,
        "data": data
    }
    if symbol:
        response["symbol"] = symbol
    return response


# =============================
# HISTORY (OHLCV)
# =============================

@router.get("/history")
def routePriceHistory(
    symbol: str = Query(..., description="VCI, FPT, VNINDEX..."),
    source: str = Query("KBS"),
    start: str = Query(None, description="2024-01-01"),
    end: str = Query(None, description="2024-05-25"),
    length: str = Query(None, description="1M, 3M, 1Y..."),
    interval: str = Query("1D", description="1m, 5m, 15m, 30m, 1H, 1D, 1W, 1M"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    source = validate_source(source)

    data = servicePriceHistory(
        symbol=symbol,
        source=source,
        start=start,
        end=end,
        length=length,
        interval=interval
    )

    return base_response(source, data, symbol)


# =============================
# INTRADAY
# =============================

@router.get("/intraday")
def routePriceIntraday(
    symbol: str = Query(..., description="VCI, FPT..."),
    source: str = Query("KBS"),
    page_size: int = Query(100, ge=1, le=1000),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    source = validate_source(source)

    data = servicePriceIntraday(
        symbol=symbol,
        source=source,
        page_size=page_size
    )

    return base_response(source, data, symbol)


# =============================
# PRICE DEPTH
# =============================

@router.get("/depth")
def routePriceDepth(
    symbol: str = Query(..., description="VCI, FPT..."),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    source = validate_source(source)

    data = servicePriceDepth(
        symbol=symbol,
        source=source
    )

    return base_response(source, data, symbol)


# =============================
# FOREX HISTORY
# =============================

@router.get("/fx/history")
def routeFxHistory(
    symbol: str = Query(..., description="JPYVND, USDVND..."),
    source: str = Query("MSN"),
    start: str = Query(None, description="2024-01-01"),
    end: str = Query(None, description="2024-05-25"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    data = serviceFxHistory(
        symbol=symbol,
        source=source,
        start=start,
        end=end
    )

    return base_response(source, data, symbol)


# =============================
# CRYPTO HISTORY
# =============================

@router.get("/crypto/history")
def routeCryptoHistory(
    symbol: str = Query(..., description="BTC, ETH..."),
    source: str = Query("MSN"),
    start: str = Query(None, description="2024-01-01"),
    end: str = Query(None, description="2024-05-25"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    data = serviceCryptoHistory(
        symbol=symbol,
        source=source,
        start=start,
        end=end
    )

    return base_response(source, data, symbol)


# =============================
# WORLD INDEX HISTORY
# =============================

@router.get("/world-index/history")
def routeWorldIndexHistory(
    symbol: str = Query(..., description="DJI, SPX, N225, IXIC, HSI..."),
    source: str = Query("MSN"),
    start: str = Query(None, description="2024-01-01"),
    end: str = Query(None, description="2024-05-25"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    data = serviceWorldIndexHistory(
        symbol=symbol,
        source=source,
        start=start,
        end=end
    )

    return base_response(source, data, symbol)
