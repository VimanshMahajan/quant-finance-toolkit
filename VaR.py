import numpy as np
import yfinance as yf
from scipy.stats import norm
import pandas as pd
import datetime


def download_data(stock, start_date, end_date):
    ticker = yf.download(stock, start=start_date, end=end_date, progress=False)
    return ticker[['Close']].rename(columns={'Close': stock})


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

    stock_data = download_data('C', start, end)

    # log returns
    stock_data['returns'] = np.log(stock_data['C'] / stock_data['C'].shift(1))
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
