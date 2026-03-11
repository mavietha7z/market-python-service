from fastapi.responses import JSONResponse
from fastapi import APIRouter, Query, Header

from app.services.price import (
    service_price_fx_history,
    service_price_stock_history,
    service_price_crypto_history,
    service_price_stock_intraday,
    service_price_world_index_history
)

DEFAULT_STOCK_SOURCE = "VCI"
VALID_STOCK_SOURCES = {"KBS", "VCI"}
FIXED_EXTERNAL_SOURCE = "MSN"

router = APIRouter(
    prefix="",
    tags=["Price"]
)


# =============================
# Helpers
# =============================
def error_response(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "message": message
        }
    )


def resolve_stock_source(source: str | None):
    """
    API cổ phiếu hỗ trợ 2 nguồn:
    - Không truyền source -> mặc định VCI
    - Có truyền -> chỉ chấp nhận KBS hoặc VCI
    """
    if source is None or source == "":
        return DEFAULT_STOCK_SOURCE

    normalizedSource = source.upper()

    if normalizedSource not in VALID_STOCK_SOURCES:
        return error_response(
            400,
            "Nguồn không hợp lệ. Các nguồn được hỗ trợ: KBS, VCI"
        )

    return normalizedSource


def resolve_fixed_source(source: str | None, fixed_source: str):
    """
    API chỉ hỗ trợ 1 nguồn cố định.
    - Không truyền -> dùng fixed_source
    - Có truyền đúng fixed_source -> chấp nhận
    - Có truyền khác -> báo lỗi
    """
    if source is None or source == "":
        return fixed_source

    normalizedSource = source.upper()
    normalizedFixedSource = fixed_source.upper()

    if normalizedSource != normalizedFixedSource:
        return error_response(
            400,
            f"API này chỉ hỗ trợ nguồn {normalizedFixedSource}"
        )

    return normalizedFixedSource


def base_response(symbol: str, source: str, data):
    return {
        "status": 200,
        "source": source,
        "symbol": symbol,
        "data": data
    }


def handle_request_stock_source(service_func, symbol, source, api_key, **kwargs):
    normalizedSymbol = symbol.upper()
    resolvedSource = resolve_stock_source(source)

    if isinstance(resolvedSource, JSONResponse):
        return resolvedSource

    data = service_func(normalizedSymbol, resolvedSource, **kwargs)

    return base_response(normalizedSymbol, resolvedSource, data)


def handle_request_fixed_source(service_func, symbol, source, fixed_source, api_key, **kwargs):
    normalizedSymbol = symbol.upper()
    resolvedSource = resolve_fixed_source(source, fixed_source)

    if isinstance(resolvedSource, JSONResponse):
        return resolvedSource

    data = service_func(normalizedSymbol, resolvedSource, **kwargs)

    return base_response(normalizedSymbol, resolvedSource, data)

# =============================
# Giá lịch sử (OHLCV)
# =============================
@router.get("/history")
def api_price_history(
    symbol: str = Query(..., description="VCI, FPT, VNINDEX..."),
    source: str | None = Query(None),
    start: str = Query(..., description="2024-01-01"),
    end: str = Query(..., description="2024-05-25"),
    interval: str = Query(..., description="1m, 5m, 15m, 30m, 1H, 1D, 1W, 1M"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_stock_source(
        service_price_stock_history,
        symbol,
        source,
        x_api_key,
        start=start,
        end=end,
        interval=interval
    )


@router.get("/intraday")
def api_price_intraday(
    symbol: str = Query(..., description="VCI, FPT..."),
    source: str | None = Query(None),
    page_size: int = Query(100, ge=1, le=1000),
    get_all: bool = Query(False, description="Lấy tất cả dữ liệu khớp lệnh (cẩn thận với tham số này)"),
    last_time: str = Query(None, description="str/int/float - thời điểm cuối cùng đã có dữ liệu (dùng để phân trang, lấy dữ liệu mới hơn)"),
    last_time_format: str = Query("iso", description="Định dạng của last_time (iso hoặc unix)"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_stock_source(
        service_price_stock_intraday,
        symbol,
        source,
        x_api_key,
        page_size=page_size,
        get_all=get_all,
        last_time=last_time,
        last_time_format=last_time_format
    )


# =============================
# Forex (FX)
# =============================
@router.get("/fx/history")
def api_price_fx_history(
    symbol: str = Query(..., description="USDVND, JPYVND, AUDVND..."),
    source: str | None = Query(None, description="Chỉ hỗ trợ MSN"),
    start: str = Query(..., description="2024-01-01"),
    end: str = Query(..., description="2024-05-25"),
    interval: str = Query("1D", description="Chỉ hỗ trợ dữ liệu hàng ngày cho forex"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_fixed_source(
        service_price_fx_history,
        symbol,
        source,
        "MSN",
        x_api_key,
        start=start,
        end=end,
        interval=interval
    )  


@router.get("/crypto/history")
def api_price_crypto_history(
    symbol: str = Query(..., description="BTC, ETH, USDT, USDC, BNB..."),
    source: str | None = Query(None, description="Chỉ hỗ trợ MSN"),
    start: str = Query(..., description="2024-01-01"),
    end: str = Query(..., description="2024-05-25"),
    interval: str = Query("1D", description="Chỉ hỗ trợ dữ liệu hàng ngày cho crypto"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_fixed_source(
        service_price_crypto_history,
        symbol,
        source,
        "MSN",
        x_api_key,
        start=start,
        end=end,
        interval=interval
    )

# =============================
# Chỉ số quốc tế
# =============================
@router.get("/world-index/history")
def api_price_world_index_history(
    symbol: str = Query(..., description="DJI, SPX, N225, IXIC, HSI..."),
    source: str | None = Query(None, description="Chỉ hỗ trợ MSN"),
    start: str = Query(..., description="2024-01-01"),
    end: str = Query(..., description="2024-05-25"),
    interval: str = Query("1D", description="Chỉ hỗ trợ dữ liệu hàng ngày cho chỉ số quốc tế"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_fixed_source(
        service_price_world_index_history,
        symbol,
        source,
        "MSN",
        x_api_key,
        start=start,
        end=end,
        interval=interval
    )
