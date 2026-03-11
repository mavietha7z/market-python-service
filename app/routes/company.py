from fastapi import APIRouter, Query, Header, HTTPException

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
        raise HTTPException(
            status_code=400,
            detail=f"Invalid source. Supported sources: {', '.join(VALID_SOURCES)}"
        )

    return source


def base_response(symbol: str, source: str, data):
    return {
        "status": "success",
        "symbol": symbol,
        "source": source,
        "data": data
    }


def handle_request(service_func, symbol, source, api_key, **kwargs):
    symbol = symbol.upper()
    source = validate_source(source)

    data = service_func(symbol, source, **kwargs)

    return base_response(symbol, source, data)


# =============================
# OVERVIEW
# =============================

@router.get("/overview")
def api_company_overview(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_overview, symbol, source, x_api_key)


# =============================
# SHAREHOLDERS
# =============================

@router.get("/shareholders")
def api_company_shareholders(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_shareholders, symbol, source, x_api_key)


# =============================
# OFFICERS
# =============================

@router.get("/officers")
def api_company_officers(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_officers, symbol, source, x_api_key)


# =============================
# SUBSIDIARIES
# =============================

@router.get("/subsidiaries")
def api_company_subsidiaries(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_subsidiaries, symbol, source, x_api_key)


# =============================
# AFFILIATE
# =============================

@router.get("/affiliate")
def api_company_affiliate(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_affiliate, symbol, source, x_api_key)


# =============================
# NEWS
# =============================

@router.get("/news")
def api_company_news(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_news, symbol, source, x_api_key)


# =============================
# EVENTS
# =============================

@router.get("/events")
def api_company_events(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_events, symbol, source, x_api_key)


# =============================
# OWNERSHIP
# =============================

@router.get("/ownership")
def api_company_ownership(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_ownership, symbol, source, x_api_key)


# =============================
# CAPITAL HISTORY
# =============================

@router.get("/capital-history")
def api_company_capital_history(
    symbol: str = Query(...),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_capital_history, symbol, source, x_api_key)


# =============================
# INSIDER TRADING
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
# REPORTS (VCI only)
# =============================

@router.get("/reports")
def api_company_reports(
    symbol: str = Query(...),
    source: str = Query("VCI"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_reports, symbol, source, x_api_key)


# =============================
# TRADING STATS (VCI only)
# =============================

@router.get("/trading-stats")
def api_company_trading_stats(
    symbol: str = Query(...),
    source: str = Query("VCI"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_trading_stats, symbol, source, x_api_key)


# =============================
# RATIO SUMMARY (VCI only)
# =============================

@router.get("/ratio-summary")
def api_company_ratio_summary(
    symbol: str = Query(...),
    source: str = Query("VCI"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(service_company_ratio_summary, symbol, source, x_api_key)