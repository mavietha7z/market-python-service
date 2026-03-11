from fastapi.responses import JSONResponse
from fastapi import APIRouter, Query, Header

from app.services.listing import (
    service_listing_all_symbols,
    service_listing_all_indices,
    service_listing_industries_icb,
    service_listing_search_symbol_id,
    service_listing_symbols_by_group,
    service_listing_indices_by_group,
    service_listing_symbols_by_exchange,
    service_listing_symbols_by_industries,
)

DEFAULT_MULTI_SOURCE = "VCI"
VALID_SOURCES = {"VCI", "KBS"}

router = APIRouter(
    prefix="",
    tags=["Listing"]
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


def resolve_multi_source(source: str | None):
    """
    API hỗ trợ 2 nguồn:
    - Không truyền source -> mặc định VCI
    - Có truyền -> chỉ chấp nhận KBS hoặc VCI
    """
    if source is None or source == "":
        return DEFAULT_MULTI_SOURCE

    normalizedSource = source.upper()

    if normalizedSource not in VALID_SOURCES:
        return error_response(
            400,
            "Nguồn không hợp lệ. Các nguồn được hỗ trợ: KBS, VCI"
        )

    return normalizedSource


def resolve_single_source(fixed_source: str):
    """
    API chỉ hỗ trợ 1 nguồn:
    - Không cần nhận source từ client
    - Luôn dùng nguồn cố định
    """
    return fixed_source.upper()


def base_response(source: str, data):
    return {
        "status": 200,
        "source": source,
        "data": data
    }


def handle_request_multi_source(service_func, source, api_key, **kwargs):
    resolvedSource = resolve_multi_source(source)

    if isinstance(resolvedSource, JSONResponse):
        return resolvedSource

    data = service_func(resolvedSource, **kwargs)

    return base_response(resolvedSource, data)


def handle_request_single_source(service_func, fixed_source, api_key, **kwargs):
    resolvedSource = resolve_single_source(fixed_source)

    data = service_func(resolvedSource, **kwargs)

    return base_response(resolvedSource, data)


# =============================
# Liệt kê tất cả mã chứng khoán (KBS và VCI)
# =============================
@router.get("/all-symbols")
def api_list_all_symbols(
    source: str | None = Query(None),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_multi_source(service_listing_all_symbols, source, x_api_key)


# =============================
# Liệt kê mã chứng khoán theo sàn (KBS và VCI)
# =============================
@router.get("/symbols-by-exchange")
def api_listing_symbols_by_exchange(
    exchange: str = Query(..., description="HOSE | HNX | UPCOM"),
    source: str | None = Query(None),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_multi_source(service_listing_symbols_by_exchange, source, x_api_key, exchange=exchange)


# =============================
# Liệt kê chứng khoán theo phân nhóm (KBS và VCI)
# =============================
@router.get("/symbols-by-group")
def api_listing_symbols_by_group(
    group: str = Query(..., description="VN30 | VN100 | ETF | ..."),
    source: str | None = Query(None),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_multi_source(service_listing_symbols_by_group, source, x_api_key, group=group)


# =============================
# Chứng khoán theo ngành (KBS và VCI)
# =============================
@router.get("/symbols-by-industries")
def api_listing_symbols_by_industries(
    source: str | None = Query(None),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_multi_source(service_listing_symbols_by_industries, source, x_api_key)


# =============================
# Phân loại ngành ICB (Chỉ VCI)
# =============================
@router.get("/industries-icb")
def api_listing_industries_icb(
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_single_source(service_listing_industries_icb, 'VCI', x_api_key)


# =============================
# Liệt kê tất cả chỉ số (KBS và VCI)
# =============================
@router.get("/all-indices")
def api_listing_all_indices(
    source: str | None = Query(None),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_multi_source(service_listing_all_indices, source, x_api_key)


# =============================
# Liệt kê chỉ số theo nhóm (KBS và VCI)
# =============================
@router.get("/indices-by-group")
def api_listing_indices_by_group(
    group: str = Query(..., description="HOSE Indices | Sector Indices | Investment Indices | VNX Indices"),
    source: str | None = Query(None),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_multi_source(service_listing_indices_by_group, source, x_api_key, group=group)


# =============================
# Tìm mã chứng khoán quốc tế (KBS và VCI)
# =============================
@router.get("/search-symbol-id")
def api_listing_search_symbol_id(
    symbol: str = Query(..., description="USD | EUR | BTC | ..."),
    source: str | None = Query(None),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_multi_source(service_listing_search_symbol_id, source, x_api_key, symbol=symbol)