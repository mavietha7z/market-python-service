from fastapi.responses import JSONResponse
from fastapi import APIRouter, Query, Header

from app.services.company import (
    service_company_news,
    service_company_events,
    service_company_reports,
    service_company_overview,
    service_company_officers,
    service_company_affiliate,
    service_company_ownership,
    service_company_shareholders,
    service_company_subsidiaries,
    service_company_trading_stats,
    service_company_ratio_summary,
    service_company_capital_history,
    service_company_insider_trading,
)

DEFAULT_MULTI_SOURCE = "KBS"
VALID_SOURCES = {"KBS", "VCI"}

router = APIRouter(
    prefix="",
    tags=["Company"]
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
    - Không truyền source -> mặc định KBS
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


def base_response(symbol: str, source: str, data):
    return {
        "status": 200,
        "source": source,
        "symbol": symbol,
        "data": data
    }


def handle_request_multi_source(service_func, symbol, source, api_key, **kwargs):
    normalizedSymbol = symbol.upper()
    resolvedSource = resolve_multi_source(source)

    if isinstance(resolvedSource, JSONResponse):
        return resolvedSource

    data = service_func(normalizedSymbol, resolvedSource, **kwargs)

    return base_response(normalizedSymbol, resolvedSource, data)


def handle_request_single_source(service_func, symbol, fixed_source, api_key, **kwargs):
    normalizedSymbol = symbol.upper()
    resolvedSource = resolve_single_source(fixed_source)

    data = service_func(normalizedSymbol, resolvedSource, **kwargs)

    return base_response(normalizedSymbol, resolvedSource, data)


# =============================
# Thông tin công ty (KBS và VCI)
# =============================
@router.get("/overview")
def api_company_overview(
    symbol: str = Query(...),
    source: str | None = Query(None),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_multi_source(
        service_company_overview,
        symbol,
        source,
        x_api_key
    )


# =============================
# Cổ đông lớn (KBS và VCI)
# =============================
@router.get("/shareholders")
def api_company_shareholders(
    symbol: str = Query(...),
    source: str | None = Query(None),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_multi_source(
        service_company_shareholders,
        symbol,
        source,
        x_api_key
    )


# =============================
# Ban lãnh đạo (KBS và VCI)
# =============================
@router.get("/officers")
def api_company_officers(
    symbol: str = Query(...),
    source: str | None = Query(None),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_multi_source(
        service_company_officers,
        symbol,
        source,
        x_api_key
    )


# =============================
# Công ty con (Chỉ KBS)
# =============================
@router.get("/subsidiaries")
def api_company_subsidiaries(
    symbol: str = Query(...),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_single_source(
        service_company_subsidiaries,
        symbol,
        "KBS",
        x_api_key
    )


# =============================
# Công ty liên kết (KBS và VCI)
# =============================
@router.get("/affiliate")
def api_company_affiliate(
    symbol: str = Query(...),
    source: str | None = Query(None),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_multi_source(
        service_company_affiliate,
        symbol,
        source,
        x_api_key
    )


# =============================
# Tin tức (KBS và VCI)
# =============================
@router.get("/news")
def api_company_news(
    symbol: str = Query(...),
    source: str | None = Query(None),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_multi_source(
        service_company_news,
        symbol,
        source,
        x_api_key
    )


# =============================
# Sự kiện (KBS và VCI)
# =============================
@router.get("/events")
def api_company_events(
    symbol: str = Query(...),
    source: str | None = Query(None),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_multi_source(
        service_company_events,
        symbol,
        source,
        x_api_key
    )


# =============================
# Cơ cấu cổ đông (Chỉ KBS)
# =============================
@router.get("/ownership")
def api_company_ownership(
    symbol: str = Query(...),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_single_source(
        service_company_ownership,
        symbol,
        "KBS",
        x_api_key
    )


# =============================
# Lịch sử vốn điều lệ (Chỉ KBS)
# =============================
@router.get("/capital-history")
def api_company_capital_history(
    symbol: str = Query(...),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_single_source(
        service_company_capital_history,
        symbol,
        "KBS",
        x_api_key
    )


# =============================
# Giao dịch nội bộ (Chỉ KBS)
# =============================
@router.get("/insider-trading")
def api_company_insider_trading(
    symbol: str = Query(...),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_single_source(
        service_company_insider_trading,
        symbol,
        "KBS",
        x_api_key,
        page=page,
        page_size=page_size
    )


# =============================
# Báo cáo phân tích (Chỉ VCI)
# =============================
@router.get("/reports")
def api_company_reports(
    symbol: str = Query(...),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_single_source(
        service_company_reports,
        symbol,
        "VCI",
        x_api_key
    )


# =============================
# Thống kê giao dịch (Chỉ VCI)
# =============================
@router.get("/trading-stats")
def api_company_trading_stats(
    symbol: str = Query(...),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_single_source(
        service_company_trading_stats,
        symbol,
        "VCI",
        x_api_key
    )


# =============================
# Tóm tắt tỷ lệ tài chính (Chỉ VCI)
# =============================
@router.get("/ratio-summary")
def api_company_ratio_summary(
    symbol: str = Query(...),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request_single_source(
        service_company_ratio_summary,
        symbol,
        "VCI",
        x_api_key
    )