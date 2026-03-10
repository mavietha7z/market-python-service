from vnstock import Vnstock
import pandas as pd
import numpy as np


def normalize_data(data):
    if isinstance(data, pd.DataFrame):
        return data.replace({np.nan: None}).to_dict(orient="records")

    if isinstance(data, pd.Series):
        return data.replace({np.nan: None}).to_dict()

    return data


def get_stock(symbol: str, source: str):
    return Vnstock().stock(symbol=symbol, source=source)


def service_company_overview(symbol: str, source: str):
    stock = get_stock(symbol, source)
    data = stock.company.overview()
    return normalize_data(data)


def service_company_shareholders(symbol: str, source: str):
    stock = get_stock(symbol, source)
    data = stock.company.shareholders()
    return normalize_data(data)


def service_company_officers(symbol: str, source: str):
    stock = get_stock(symbol, source)
    data = stock.company.officers()
    return normalize_data(data)


def service_company_subsidiaries(symbol: str, source: str):
    stock = get_stock(symbol, source)
    data = stock.company.subsidiaries()
    return normalize_data(data)


def service_company_affiliate(symbol: str, source: str):
    stock = get_stock(symbol, source)
    data = stock.company.affiliate()
    return normalize_data(data)


def service_company_news(symbol: str, source: str):
    stock = get_stock(symbol, source)
    data = stock.company.news()
    return normalize_data(data)


def service_company_events(symbol: str, source: str):
    stock = get_stock(symbol, source)
    data = stock.company.events()
    return normalize_data(data)


def service_company_ownership(symbol: str, source: str):
    stock = get_stock(symbol, source)
    data = stock.company.ownership()
    return normalize_data(data)


def service_company_capital_history(symbol: str, source: str):
    stock = get_stock(symbol, source)
    data = stock.company.capital_history()
    return normalize_data(data)


def service_company_insider_trading(symbol: str, source: str):
    stock = get_stock(symbol, source)
    data = stock.company.insider_trading()
    return normalize_data(data)


def service_company_reports(symbol: str, source: str):
    stock = get_stock(symbol, source)
    data = stock.company.reports()
    return normalize_data(data)


def service_company_trading_stats(symbol: str, source: str):
    stock = get_stock(symbol, source)
    data = stock.company.trading_stats()
    return normalize_data(data)


def service_company_ratio_summary(symbol: str, source: str):
    stock = get_stock(symbol, source)
    data = stock.company.ratio_summary()
    return normalize_data(data)