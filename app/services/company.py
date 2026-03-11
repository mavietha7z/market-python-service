import numpy as np
import pandas as pd
from vnstock import Vnstock
from fastapi import HTTPException


# ============================
# Data Normalizer
# ============================
def normalize_data(data):
    if data is None:
        return None

    if isinstance(data, pd.DataFrame):
        df = data.replace({
            np.nan: None,
            pd.NaT: None,
            np.inf: None,
            -np.inf: None
        })

        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].apply(
                    lambda x: x.isoformat() if x is not None else None
                )

        return df.to_dict(orient="records")

    if isinstance(data, pd.Series):
        series = data.replace({
            np.nan: None,
            pd.NaT: None,
            np.inf: None,
            -np.inf: None
        })

        return series.to_dict()

    if isinstance(data, (dict, list)):
        return data

    return data


# ============================
# VNStock Instance
# ============================
def get_stock(symbol: str, source: str):
    try:
        return Vnstock().stock(
            symbol=symbol.upper(),
            source=source
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"{str(error)}"
        )


# ============================
# Generic Handler - calls through data_source
# ============================
def fetch_company_data(symbol: str, source: str, method: str, **kwargs):
    try:
        stock = get_stock(symbol, source)
        company = stock.company
        data_source = company.data_source

        if not hasattr(data_source, method):
            raise HTTPException(
                status_code=400,
                detail=f"Phương thức '{method}' không được hỗ trợ cho nguồn '{source}'"
            )

        functionObject = getattr(data_source, method)

        if kwargs:
            data = functionObject(**kwargs)
        else:
            data = functionObject()

        return normalize_data(data)

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi lấy dữ liệu công ty: {str(error)}"
        )


# ============================
# Service Functions
# ============================
def service_company_overview(symbol, source):
    return fetch_company_data(symbol, source, "overview")


def service_company_shareholders(symbol, source):
    return fetch_company_data(symbol, source, "shareholders")


def service_company_officers(symbol, source):
    return fetch_company_data(symbol, source, "officers")


def service_company_subsidiaries(symbol, source):
    return fetch_company_data(symbol, source, "subsidiaries")


def service_company_affiliate(symbol, source):
    return fetch_company_data(symbol, source, "affiliate")


def service_company_news(symbol, source):
    return fetch_company_data(symbol, source, "news")


def service_company_events(symbol, source):
    return fetch_company_data(symbol, source, "events")


def service_company_insider_trading(symbol, source, page=1, page_size=10):
    return fetch_company_data(symbol, source, "insider_trading", page=page, page_size=page_size)


def service_company_ownership(symbol, source):
    return fetch_company_data(symbol, source, "ownership")


def service_company_capital_history(symbol, source):
    return fetch_company_data(symbol, source, "capital_history")


def service_company_reports(symbol, source):
    return fetch_company_data(symbol, source, "reports")


def service_company_trading_stats(symbol, source):
    return fetch_company_data(symbol, source, "trading_stats")


def service_company_ratio_summary(symbol, source):
    return fetch_company_data(symbol, source, "ratio_summary")