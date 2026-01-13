import numpy as np
import yfinance as yf
from scipy.stats import norm
import pandas as pd
import datetime


def download_data(stock, start_date, end_date):
    """Download price data for `stock` and return a single-column DataFrame.

    yfinance may return either single-index columns or MultiIndex columns.
    Prefer 'Adj Close' when available, otherwise fall back to 'Close'.
    """
    ticker = yf.download(stock, start=start_date, end=end_date, progress=False)

    if ticker is None or len(ticker) == 0:
        raise ValueError(f"No data returned for ticker '{stock}'.")

    price_field_candidates = ("Adj Close", "Close")

    if isinstance(ticker.columns, pd.MultiIndex):
        col = None
        for field in price_field_candidates:
            if (field, stock) in ticker.columns:
                col = (field, stock)
                break
            if (stock, field) in ticker.columns:
                col = (stock, field)
                break

        if col is None:
            raise KeyError(
                f"Couldn't find a Close/Adj Close series for '{stock}'. Available columns: {list(ticker.columns)[:10]}..."
            )

        prices = ticker[col]
    else:
        field = next((f for f in price_field_candidates if f in ticker.columns), None)
        if field is None:
            raise KeyError(
                f"Couldn't find 'Close' or 'Adj Close' in downloaded data for '{stock}'. Available columns: {ticker.columns.tolist()}"
            )
        prices = ticker[field]

    return prices.to_frame(name=stock)


# 1-day VaR
def calculate_var(position, c, mu, sigma):
    z = norm.ppf(c)
    var = position * (z * sigma - mu)
    return var


# n-day VaR (square-root-of-time rule)
def calculate_var_n(position, c, mu, sigma, n):
    z = norm.ppf(c)
    var = position * (z * sigma * np.sqrt(n) - mu * n)
    return var


if __name__ == '__main__':

    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime(2026, 1, 1)

    stock = 'C'
    stock_data = download_data(stock, start, end)

    # log returns
    stock_data['returns'] = np.log(stock_data[stock] / stock_data[stock].shift(1))
    stock_data.dropna(inplace=True)

    # investment value
    S = 1_000_000  # $1M

    # confidence level
    c = 0.99

    # daily return parameters
    mu = stock_data['returns'].mean()
    sigma = stock_data['returns'].std(ddof=1)

    var_1d = calculate_var_n(S, c, mu, sigma, 1)

    print(f"1-day 99% VaR: ${var_1d:,.2f}")
