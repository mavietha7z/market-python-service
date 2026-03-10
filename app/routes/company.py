from fastapi import APIRouter
from app.services.company import *

from fastapi import APIRouter, Depends, Query
from app.core.auth import verify_api_key
from app.services.company import service_company_overview

router = APIRouter(
    prefix="/company",
    tags=["Company"]
)


@router.get("/overview")
def company_overview(
        symbol: str,
        source: str = Query("VCI"),
        api_key: str = Depends(verify_api_key)
):
    return service_company_overview(symbol, source)


router = APIRouter(prefix="/company", tags=["Company"])


# =============================
# OVERVIEW
# =============================

@router.get("/overview")
def api_company_overview(symbol: str, source: str = "KBS"):
    return service_company_overview(symbol, source)


# =============================
# SHAREHOLDERS
# =============================

@router.get("/shareholders")
def api_company_shareholders(symbol: str, source: str = "KBS"):
    return service_company_shareholders(symbol, source)


# =============================
# OFFICERS
# =============================

@router.get("/officers")
def api_company_officers(symbol: str, source: str = "KBS"):
    return service_company_officers(symbol, source)


# =============================
# SUBSIDIARIES
# =============================

@router.get("/subsidiaries")
def api_company_subsidiaries(symbol: str, source: str = "KBS"):
    return service_company_subsidiaries(symbol, source)


# =============================
# AFFILIATE
# =============================

@router.get("/affiliate")
def api_company_affiliate(symbol: str, source: str = "KBS"):
    return service_company_affiliate(symbol, source)


# =============================
# NEWS
# =============================

@router.get("/news")
def api_company_news(symbol: str, source: str = "KBS"):
    return service_company_news(symbol, source)


# =============================
# EVENTS
# =============================

@router.get("/events")
def api_company_events(symbol: str, source: str = "KBS"):
    return service_company_events(symbol, source)


# =============================
# OWNERSHIP
# =============================

@router.get("/ownership")
def api_company_ownership(symbol: str, source: str = "KBS"):
    return service_company_ownership(symbol, source)


# =============================
# CAPITAL HISTORY
# =============================

@router.get("/capital-history")
def api_company_capital_history(symbol: str, source: str = "KBS"):
    return service_company_capital_history(symbol, source)


# =============================
# INSIDER TRADING
# =============================

@router.get("/insider-trading")
def api_company_insider_trading(symbol: str, source: str = "KBS"):
    return service_company_insider_trading(symbol, source)


# =============================
# REPORTS
# =============================

@router.get("/reports")
def api_company_reports(symbol: str, source: str = "KBS"):
    return service_company_reports(symbol, source)


# =============================
# TRADING STATS
# =============================

@router.get("/trading-stats")
def api_company_trading_stats(symbol: str, source: str = "KBS"):
    return service_company_trading_stats(symbol, source)


# =============================
# RATIO SUMMARY
# =============================

@router.get("/ratio-summary")
def api_company_ratio_summary(symbol: str, source: str = "KBS"):
    return service_company_ratio_summary(symbol, source)