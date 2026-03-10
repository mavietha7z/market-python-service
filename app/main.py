import os

from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException, Header
from pydantic import BaseModel
from vnstock import Vnstock


load_dotenv()

app = FastAPI(
    title="Market Python Service",
    version="1.0.0"
)

internalApiKey = os.getenv("INTERNAL_API_KEY", "")


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

    try:
        stock = Vnstock().stock(symbol=symbol.upper(), source="VCI")
        dataFrame = stock.quote.history(
            start=start,
            end=end,
            interval=interval
        )

        items = dataFrame.to_dict(orient="records")

        return {
            "success": True,
            "symbol": symbol.upper(),
            "start": start,
            "end": end,
            "interval": interval,
            "count": len(items),
            "items": items
        }
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
        try:
            stock = Vnstock().stock(symbol=symbol.upper(), source="VCI")
            dataFrame = stock.quote.history(
                start=payload.start,
                end=payload.end,
                interval=payload.interval
            )

            items = dataFrame.to_dict(orient="records")

            results.append({
                "success": True,
                "symbol": symbol.upper(),
                "start": payload.start,
                "end": payload.end,
                "interval": payload.interval,
                "count": len(items),
                "items": items
            })
        except Exception as error:
            results.append({
                "success": False,
                "symbol": symbol.upper(),
                "error": str(error)
            })

    return {
        "success": True,
        "count": len(results),
        "results": results
    }