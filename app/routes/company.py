from fastapi import APIRouter, Query, HTTPException, Header
from app.core.auth import verify_api_key
from app.services.company import (
    service_company_overview,
    service_company_shareholders,
    service_company_officers,
    service_company_subsidiaries,
    service_company_affiliate,
    service_company_news,
    service_company_events,
    service_company_ownership,
    service_company_capital_history,
    service_company_insider_trading,
    service_company_reports,
    service_company_trading_stats,
    service_company_ratio_summary,
)

# Các nguồn dữ liệu được hỗ trợ
VALID_SOURCES = ["KBS", "VCI"]

router = APIRouter(
    prefix="/company",
    tags=["Company"]
)


def validate_source(source: str) -> str:
    """Validate source parameter"""
    if source not in VALID_SOURCES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid source. Supported sources: {', '.join(VALID_SOURCES)}"
        )
    return source


def success_response(data, message: str = "Success"):
    """Wrapper response chuẩn hóa"""
    return {
        "success": True,
        "message": message,
        "data": data
    }


# =============================
# OVERVIEW
# =============================

@router.get("/overview")
def api_company_overview(
    symbol: str = Query(..., description="Mã cổ phiếu, ví dụ: TCB"),
    source: str = Query("KBS", description=f"Nguồn dữ liệu: {', '.join(VALID_SOURCES)}"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    verify_api_key(x_api_key)
    source = validate_source(source)
    data = service_company_overview(symbol, source)
    return success_response(data)


# =============================
# SHAREHOLDERS
# =============================

@router.get("/shareholders")
def api_company_shareholders(
    symbol: str = Query(..., description="Mã cổ phiếu"),
    source: str = Query("KBS", description=f"Nguồn dữ liệu: {', '.join(VALID_SOURCES)}"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    verify_api_key(x_api_key)
    source = validate_source(source)
    data = service_company_shareholders(symbol, source)
    return success_response(data)


# =============================
# OFFICERS
# =============================

@router.get("/officers")
def api_company_officers(
    symbol: str = Query(..., description="Mã cổ phiếu"),
    source: str = Query("KBS", description=f"Nguồn dữ liệu: {', '.join(VALID_SOURCES)}"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    verify_api_key(x_api_key)
    source = validate_source(source)
    data = service_company_officers(symbol, source)
    return success_response(data)


# =============================
# SUBSIDIARIES
# =============================

@router.get("/subsidiaries")
def api_company_subsidiaries(
    symbol: str = Query(..., description="Mã cổ phiếu"),
    source: str = Query("KBS", description=f"Nguồn dữ liệu: {', '.join(VALID_SOURCES)}"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    verify_api_key(x_api_key)
    source = validate_source(source)
    data = service_company_subsidiaries(symbol, source)
    return success_response(data)


# =============================
# AFFILIATE
# =============================

@router.get("/affiliate")
def api_company_affiliate(
    symbol: str = Query(..., description="Mã cổ phiếu"),
    source: str = Query("KBS", description=f"Nguồn dữ liệu: {', '.join(VALID_SOURCES)}"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    verify_api_key(x_api_key)
    source = validate_source(source)
    data = service_company_affiliate(symbol, source)
    return success_response(data)


# =============================
# NEWS
# =============================

@router.get("/news")
def api_company_news(
    symbol: str = Query(..., description="Mã cổ phiếu"),
    source: str = Query("KBS", description=f"Nguồn dữ liệu: {', '.join(VALID_SOURCES)}"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    verify_api_key(x_api_key)
    source = validate_source(source)
    data = service_company_news(symbol, source)
    return success_response(data)


# =============================
# EVENTS
# =============================

@router.get("/events")
def api_company_events(
    symbol: str = Query(..., description="Mã cổ phiếu"),
    source: str = Query("KBS", description=f"Nguồn dữ liệu: {', '.join(VALID_SOURCES)}"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    verify_api_key(x_api_key)
    source = validate_source(source)
    data = service_company_events(symbol, source)
    return success_response(data)


# =============================
# OWNERSHIP
# =============================

@router.get("/ownership")
def api_company_ownership(
    symbol: str = Query(..., description="Mã cổ phiếu"),
    source: str = Query("KBS", description=f"Nguồn dữ liệu: {', '.join(VALID_SOURCES)}"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    verify_api_key(x_api_key)
    source = validate_source(source)
    data = service_company_ownership(symbol, source)
    return success_response(data)


# =============================
# CAPITAL HISTORY
# =============================

@router.get("/capital-history")
def api_company_capital_history(
    symbol: str = Query(..., description="Mã cổ phiếu"),
    source: str = Query("KBS", description=f"Nguồn dữ liệu: {', '.join(VALID_SOURCES)}"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    verify_api_key(x_api_key)
    source = validate_source(source)
    data = service_company_capital_history(symbol, source)
    return success_response(data)


# =============================
# INSIDER TRADING
# =============================

@router.get("/insider-trading")
def api_company_insider_trading(
    symbol: str = Query(..., description="Mã cổ phiếu"),
    source: str = Query("KBS", description=f"Nguồn dữ liệu: {', '.join(VALID_SOURCES)}"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    verify_api_key(x_api_key)
    source = validate_source(source)
    data = service_company_insider_trading(symbol, source)
    return success_response(data)


# =============================
# REPORTS
# =============================

@router.get("/reports")
def api_company_reports(
    symbol: str = Query(..., description="Mã cổ phiếu"),
    source: str = Query("KBS", description=f"Nguồn dữ liệu: {', '.join(VALID_SOURCES)}"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    verify_api_key(x_api_key)
    source = validate_source(source)
    data = service_company_reports(symbol, source)
    return success_response(data)


# =============================
# TRADING STATS
# =============================

@router.get("/trading-stats")
def api_company_trading_stats(
    symbol: str = Query(..., description="Mã cổ phiếu"),
    source: str = Query("KBS", description=f"Nguồn dữ liệu: {', '.join(VALID_SOURCES)}"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    verify_api_key(x_api_key)
    source = validate_source(source)
    data = service_company_trading_stats(symbol, source)
    return success_response(data)


# =============================
# RATIO SUMMARY
# =============================

@router.get("/ratio-summary")
def api_company_ratio_summary(
    symbol: str = Query(..., description="Mã cổ phiếu"),
    source: str = Query("KBS", description=f"Nguồn dữ liệu: {', '.join(VALID_SOURCES)}"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    verify_api_key(x_api_key)
    source = validate_source(source)
    data = service_company_ratio_summary(symbol, source)
    return success_response(data)
