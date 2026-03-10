import os

from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException, Header
from pydantic import BaseModel
from vnstock import Vnstock
from cachetools import TTLCache

load_dotenv()

app = FastAPI(
    title="Market Python Service",
    version="1.0.0"
)

internalApiKey = os.getenv("INTERNAL_API_KEY", "")

# Cache RAM
# maxsize = số request cache
# ttl = 300s = 5 phút
cache = TTLCache(maxsize=1000, ttl=300)


def verifyApiKey(xApiKey: str | None):
    if internalApiKey and xApiKey != internalApiKey:
        raise HTTPException(status_code=401, detail="Unauthorized")


class StockHistoryBatchRequest(BaseModel):
    symbols: list[str]
    start: str
    end: str
    interval: str = "1D"


@app.get("/")
def root():
    return {
        "message": "Python market service is running"
    }


@app.get("/health")
def health(x_api_key: str | None = Header(default=None)):
    verifyApiKey(x_api_key)

    return {
        "status": "ok"
    }


@app.get("/stocks/history")
def getStockHistory(
    symbol: str = Query(..., description="Ví dụ: TCB"),
    start: str = Query(..., description="YYYY-MM-DD"),
    end: str = Query(..., description="YYYY-MM-DD"),
    interval: str = Query("1D", description="Ví dụ: 1D"),
    x_api_key: str | None = Header(default=None)
):
    verifyApiKey(x_api_key)

    symbol = symbol.upper()

    # Cache key
    cache_key = f"history:{symbol}:{start}:{end}:{interval}"

    if cache_key in cache:
        return cache[cache_key]

    try:
        stock = Vnstock().stock(symbol=symbol, source="VCI")

        dataFrame = stock.quote.history(
            start=start,
            end=end,
            interval=interval
        )

        items = dataFrame.to_dict(orient="records")

        response = {
            "success": True,
            "symbol": symbol,
            "start": start,
            "end": end,
            "interval": interval,
            "count": len(items),
            "items": items
        }

        cache[cache_key] = response

        return response

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/stocks/history/batch")
def getStockHistoryBatch(
    payload: StockHistoryBatchRequest,
    x_api_key: str | None = Header(default=None)
):
    verifyApiKey(x_api_key)

    results = []

    for symbol in payload.symbols:
        symbol = symbol.upper()

        cache_key = f"history:{symbol}:{payload.start}:{payload.end}:{payload.interval}"

        # Nếu có cache thì dùng luôn
        if cache_key in cache:
            results.append(cache[cache_key])
            continue

        try:
            stock = Vnstock().stock(symbol=symbol, source="VCI")

            dataFrame = stock.quote.history(
                start=payload.start,
                end=payload.end,
                interval=payload.interval
            )

            items = dataFrame.to_dict(orient="records")

            response = {
                "success": True,
                "symbol": symbol,
                "start": payload.start,
                "end": payload.end,
                "interval": payload.interval,
                "count": len(items),
                "items": items
            }

            cache[cache_key] = response

            results.append(response)

        except Exception as error:
            results.append({
                "success": False,
                "symbol": symbol,
                "error": str(error)
            })

    return {
        "success": True,
        "count": len(results),
        "results": results
    }