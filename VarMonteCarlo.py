import numpy as np
import yfinance as yf
import datetime
import pandas as pd


def download_data(stock, start, end):
    """Download price data and return a single-column DataFrame named with the ticker.

    Handles yfinance returning either single-index columns or MultiIndex columns.
    Prefers 'Adj Close' when available, otherwise falls back to 'Close'.
    """
    ticker = yf.download(stock, start=start, end=end, progress=False)

    if ticker is None or len(ticker) == 0:
        raise ValueError(f"No data returned for ticker '{stock}'.")

    price_field_candidates = ("Adj Close", "Close")

    # yfinance can return MultiIndex columns in some configurations.
    if isinstance(ticker.columns, pd.MultiIndex):
        # Try common layouts: (field, ticker) and (ticker, field)
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
        # Single-index columns
        field = next((f for f in price_field_candidates if f in ticker.columns), None)
        if field is None:
            raise KeyError(
                f"Couldn't find 'Close' or 'Adj Close' in downloaded data for '{stock}'. Available columns: {ticker.columns.tolist()}"
            )
        prices = ticker[field]

    return prices.to_frame(name=stock)


class ValueAtRiskMonteCarlo:

    def __init__(self, S, mu, sigma, c, n, iterations):
        self.S = S
        self.mu = mu
        self.sigma = sigma
        self.c = c
        self.n = n
        self.iterations = iterations

    def simulation(self):
        # generate random shocks
        rand = np.random.normal(0, 1, self.iterations)

        # GBM stock price simulation
        stock_prices = self.S * np.exp(
            self.n * (self.mu - 0.5 * self.sigma ** 2)
            + self.sigma * np.sqrt(self.n) * rand
        )

        # lower tail percentile
        percentile_price = np.percentile(stock_prices, (1 - self.c) * 100)

        # VaR is the potential loss
        return self.S - percentile_price


if __name__ == "__main__":

    S = 1_000_000      # investment value
    c = 0.95           # confidence level
    n = 1              # 1 day
    iterations = 100_000

    start_date = datetime.datetime(2014, 1, 1)
    end_date = datetime.datetime(2024, 10, 15)

    stock = 'C'

    # download data
    citi = download_data(stock, start_date, end_date)

    # log returns (IMPORTANT)
    citi['returns'] = np.log(citi[stock] / citi[stock].shift(1))
    citi.dropna(inplace=True)

    mu = citi['returns'].mean()
    sigma = citi['returns'].std(ddof=1)

    model = ValueAtRiskMonteCarlo(S, mu, sigma, c, n, iterations)

    print(f"Value at Risk (Monte Carlo, {int(c*100)}%): ${model.simulation():,.2f}")
