from fastapi import APIRouter, Query, Header, HTTPException

from app.services.listing import (
    serviceListingAllSymbols,
    serviceListingSymbolsByExchange,
    serviceListingSymbolsByGroup,
    serviceListingSymbolsByIndustries,
    serviceListingIndustriesICB,
    serviceListingAllIndices
)

VALID_SOURCES = {"KBS", "VCI"}

router = APIRouter(
    prefix="/listing",
    tags=["Listing"]
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


def base_response(source: str, data):
    return {
        "status": "success",
        "source": source,
        "data": data
    }


def handle_request(service_func, source, *args):
    source = validate_source(source)

    data = service_func(source, *args)

    return base_response(source, data)


# =============================
# ALL SYMBOLS
# =============================

@router.get("/all-symbols")
def routeListingAllSymbols(
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(serviceListingAllSymbols, source)


# =============================
# SYMBOLS BY EXCHANGE
# =============================

@router.get("/symbols-by-exchange")
def routeListingSymbolsByExchange(
    exchange: str = Query(..., description="HOSE | HNX | UPCOM"),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(serviceListingSymbolsByExchange, source, exchange)


# =============================
# SYMBOLS BY GROUP
# =============================

@router.get("/symbols-by-group")
def routeListingSymbolsByGroup(
    group: str = Query(..., description="VN30 | VN100 | ETF | ..."),
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(serviceListingSymbolsByGroup, source, group)


# =============================
# SYMBOLS BY INDUSTRIES
# =============================

@router.get("/symbols-by-industries")
def routeListingSymbolsByIndustries(
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(serviceListingSymbolsByIndustries, source)


# =============================
# INDUSTRIES ICB
# =============================

@router.get("/industries-icb")
def routeListingIndustriesICB(
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(serviceListingIndustriesICB, source)


# =============================
# ALL INDICES
# =============================

@router.get("/all-indices")
def routeListingAllIndices(
    source: str = Query("KBS"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    return handle_request(serviceListingAllIndices, source)