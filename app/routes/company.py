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

VALID_SOURCES = {"KBS", "VCI"}

router = APIRouter(
    prefix="",
    tags=["Company"]
)


# =============================
# Helpers
# =============================
def validate_source(source: str) -> str:
    source = source.upper()

    if source not in VALID_SOURCES:
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "message": "Nguồn không hợp lệ. Các nguồn được hỗ trợ: " + ", ".join(VALID_SOURCES)
            }
        )

    return source


def base_response(symbol: str, source: str, data):
    return {
        "status": 200,
        "source": source,
        "symbol": symbol,
        "data": data
    }


def handle_request(service_func, symbol, source, api_key, **kwargs):
    symbol = symbol.upper()
    source = validate_source(source)

    data = service_func(symbol, source, **kwargs)

    return base_response(symbol, source, data)


# =============================
# Thông tin công ty (KBS và VCI)
# =============================
@router.get("/overview")
def api_company_overview(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_overview, symbol, source, x_api_key)


# =============================
# Cổ đông lớn (KBS và VCI)
# =============================
@router.get("/shareholders")
def api_company_shareholders(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_shareholders, symbol, source, x_api_key)


# =============================
# Ban lãnh đạo (KBS và VCI)
# =============================
@router.get("/officers")
def api_company_officers(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_officers, symbol, source, x_api_key)


# =============================
# Công ty con (Chỉ KBS)
# =============================
@router.get("/subsidiaries")
def api_company_subsidiaries(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_subsidiaries, symbol, source, x_api_key)


# =============================
# Công ty liên kết (KBS và VCI)
# =============================
@router.get("/affiliate")
def api_company_affiliate(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_affiliate, symbol, source, x_api_key)


# =============================
# Tin tức (KBS và VCI)
# =============================
@router.get("/news")
def api_company_news(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_news, symbol, source, x_api_key)


# =============================
# Sự kiện (KBS và VCI)
# =============================
@router.get("/events")
def api_company_events(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_events, symbol, source, x_api_key)


# =============================
# Cơ cấu cổ đông (Chỉ KBS)
# =============================
@router.get("/ownership")
def api_company_ownership(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_ownership, symbol, source, x_api_key)


# =============================
# Lịch sử vốn điều lệ (Chỉ KBS)
# =============================
@router.get("/capital-history")
def api_company_capital_history(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_capital_history, symbol, source, x_api_key)


# =============================
# Giao dịch nội bộ (Chỉ KBS)
# =============================
@router.get("/insider-trading")
def api_company_insider_trading(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_insider_trading, symbol, source, x_api_key, page=page, page_size=page_size)


# =============================
# Báo cáo phân tích (Chỉ VCI)
# =============================
@router.get("/reports")
def api_company_reports(
    symbol: str = Query(...),
    source: str = Query("VCI"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_reports, symbol, source, x_api_key)


# =============================
# Thống kê giao dịch (Chỉ VCI)
# =============================
@router.get("/trading-stats")
def api_company_trading_stats(
    symbol: str = Query(...),
    source: str = Query("VCI"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_trading_stats, symbol, source, x_api_key)


# =============================
# Tóm tắt tỷ lệ tài chính (Chỉ VCI)
# =============================
@router.get("/ratio-summary")
def api_company_ratio_summary(
    symbol: str = Query(...),
    source: str = Query("VCI"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_ratio_summary, symbol, source, x_api_key)