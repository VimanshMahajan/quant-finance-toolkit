import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optimization
from pathlib import Path

# on average there are 252 trading days in a year
NUM_TRADING_DAYS = 252
# we will generate random w (different portfolios)
NUM_PORTFOLIOS = 10000

# stocks we are going to handle
stocks = ['MOTHERSON.NS', 'RVNL.NS', 'JPPOWER.NS', 'HINDCOPPER.NS', 'BEL.NS', 'ITC.NS']

# historical data - define START and END dates
start_date = '2018-11-11'
end_date = '2025-01-01'

# --- Output configuration ---
RESULTS_DIR = Path(__file__).parent / 'results'
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_PATH = RESULTS_DIR / 'markowitz_summary.txt'


def _write_to_summary(lines):
    """Append lines (str or list of str) to the summary file."""
    if isinstance(lines, str):
        lines = [lines]
    with open(SUMMARY_PATH, 'a', encoding='utf-8') as f:
        for line in lines:
            f.write(str(line).rstrip() + '\n')


def download_data():
    # name of the stock (key) - stock values (2010-1017) as the values
    stock_data = {}

    for stock in stocks:
        # closing prices
        ticker = yf.Ticker(stock)
        # yfinance returns column 'Close' with capital C.
        hist = ticker.history(start=start_date, end=end_date)
        if 'Close' not in hist.columns:
            # Write a note for debugging when data is missing
            _write_to_summary(f"Warning: 'Close' column not found for {stock}. Available columns: {list(hist.columns)}")
        stock_data[stock] = hist['Close'] if 'Close' in hist.columns else pd.Series(dtype=float)

    return pd.DataFrame(stock_data)


def show_data(data):
    ax = data.plot(figsize=(10, 5))
    fig = ax.get_figure()
    fig.tight_layout()
    fig_path = RESULTS_DIR / 'prices.png'
    fig.savefig(fig_path)
    plt.show()
    _write_to_summary(f"Saved price chart to: {fig_path}")


def calculate_return(data):
    # NORMALIZATION - to measure all variables in comparable metric
    log_return = np.log(data / data.shift(1))
    return log_return[1:]


def show_statistics(returns):
    # instead of daily metrics we are after annual metrics
    # mean of annual return
    annual_means = returns.mean() * NUM_TRADING_DAYS
    annual_cov = returns.cov() * NUM_TRADING_DAYS
    print(annual_means)
    print(annual_cov)
    _write_to_summary(["Annual mean returns:", str(annual_means), "", "Annual covariance matrix:", str(annual_cov), ""])


def show_mean_variance(returns, weights):
    # we are after the annual return
    portfolio_return = np.sum(returns.mean() * weights) * NUM_TRADING_DAYS
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov()
                                                            * NUM_TRADING_DAYS, weights)))
    print("Expected portfolio mean (return): ", portfolio_return)
    print("Expected portfolio volatility (standard deviation): ", portfolio_volatility)
    _write_to_summary([
        f"Expected portfolio mean (return): {portfolio_return}",
        f"Expected portfolio volatility (std): {portfolio_volatility}",
        "",
    ])


def show_portfolios(returns, volatilities):
    plt.figure(figsize=(10, 6))
    plt.scatter(volatilities, returns, c=returns / volatilities, marker='o')
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')
    fig_path = RESULTS_DIR / 'random_portfolios.png'
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.show()
    _write_to_summary(f"Saved random portfolios chart to: {fig_path}")


def generate_portfolios(returns):
    portfolio_means = []
    portfolio_risks = []
    portfolio_weights = []

    for _ in range(NUM_PORTFOLIOS):
        w = np.random.random(len(stocks))
        w /= np.sum(w)
        portfolio_weights.append(w)
        portfolio_means.append(np.sum(returns.mean() * w) * NUM_TRADING_DAYS)
        portfolio_risks.append(np.sqrt(np.dot(w.T, np.dot(returns.cov()
                                                          * NUM_TRADING_DAYS, w))))

    return np.array(portfolio_weights), np.array(portfolio_means), np.array(portfolio_risks)


def statistics(weights, returns):
    portfolio_return = np.sum(returns.mean() * weights) * NUM_TRADING_DAYS
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov()
                                                            * NUM_TRADING_DAYS, weights)))
    return np.array([portfolio_return, portfolio_volatility,
                     portfolio_return / portfolio_volatility])


# scipy optimize module can find the minimum of a given function
# the maximum of a f(x) is the minimum of -f(x)
def min_function_sharpe(weights, returns):
    return -statistics(weights, returns)[2]


# what are the constraints? The sum of weights = 1 !!!
# f(x)=0 this is the function to minimize
def optimize_portfolio(weights, returns):
    # the sum of weights is 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    # the weights can be 1 at most: 1 when 100% of money is invested into a single stock
    bounds = tuple((0, 1) for _ in range(len(stocks)))
    return optimization.minimize(fun=min_function_sharpe, x0=weights[0], args=returns
                                 , method='SLSQP', bounds=bounds, constraints=constraints)


def print_optimal_portfolio(optimum, returns):
    weights = optimum['x'].round(3)
    stats = statistics(weights, returns)
    print("Optimal portfolio: ", weights)
    print("Expected return, volatility and Sharpe ratio: ", stats)
    _write_to_summary([
        "Optimal portfolio weights:",
        str(pd.Series(weights, index=stocks)),
        "",
        "Optimal portfolio stats [return, volatility, sharpe]:",
        str(pd.Series(stats, index=['return', 'volatility', 'sharpe'])),
        "",
    ])


def show_optimal_portfolio(opt, rets, portfolio_rets, portfolio_vols):
    plt.figure(figsize=(10, 6))
    plt.scatter(portfolio_vols, portfolio_rets, c=portfolio_rets / portfolio_vols, marker='o')
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.plot(statistics(opt['x'], rets)[1], statistics(opt['x'], rets)[0], 'g*', markersize=20.0)
    fig_path = RESULTS_DIR / 'optimal_portfolio.png'
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.show()
    _write_to_summary(f"Saved optimal portfolio chart to: {fig_path}")


if __name__ == '__main__':
    # Clear previous summary
    try:
        SUMMARY_PATH.unlink(missing_ok=True)
    except Exception:
        pass

    _write_to_summary("Markowitz Portfolio Analysis Summary")
    _write_to_summary("===============================")
    _write_to_summary([f"Stocks: {stocks}", f"Start: {start_date}", f"End: {end_date}", ""])

    dataset = download_data()
    show_data(dataset)
    log_daily_returns = calculate_return(dataset)
    show_statistics(log_daily_returns)

    pweights, means, risks = generate_portfolios(log_daily_returns)
    show_portfolios(means, risks)
    optimum = optimize_portfolio(pweights, log_daily_returns)
    print_optimal_portfolio(optimum, log_daily_returns)
    show_optimal_portfolio(optimum, log_daily_returns, means, risks)

    _write_to_summary("Analysis complete.")
