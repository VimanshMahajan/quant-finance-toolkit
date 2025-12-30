# QuantFin - Quantitative Finance Library

A comprehensive Python library implementing various quantitative finance models, including option pricing, portfolio optimization, stochastic processes, and bond valuation.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Modules](#modules)
- [Usage Examples](#usage-examples)
- [Requirements](#requirements)
- [Project Structure](#project-structure)

## 🎯 Overview

QuantFin is a collection of quantitative finance implementations in Python, covering fundamental concepts in:
- Option pricing (Black-Scholes and Monte Carlo methods)
- Portfolio optimization (Markowitz Portfolio Theory)
- Stochastic processes (Wiener Process, Geometric Brownian Motion)
- Asset pricing models (CAPM)
- Bond valuation (Zero-Coupon and Coupon Bonds)
- Time value of money calculations

## ✨ Features

### Option Pricing
- **Black-Scholes Model**: Analytical solution for European call and put options
- **Monte Carlo Simulation**: Numerical pricing for options using Monte Carlo methods
- **Stock Price Simulation**: Monte Carlo simulation of stock price paths

### Portfolio Management
- **Markowitz Portfolio Optimization**: Modern Portfolio Theory implementation
- **CAPM (Capital Asset Pricing Model)**: Beta calculation and expected return estimation
- **Risk-Return Analysis**: Efficient frontier visualization

### Stochastic Processes
- **Wiener Process**: Brownian motion simulation
- **Geometric Brownian Motion (GBM)**: Stock price modeling

### Fixed Income
- **Zero-Coupon Bonds**: Present value calculations
- **Coupon Bonds**: Bond valuation with periodic coupon payments
- **Time Value of Money**: Discrete and continuous compounding

## 🚀 Installation

### Prerequisites

Python 3.7 or higher

### Required Packages

```bash
pip install numpy pandas matplotlib scipy yfinance
```

Or install from a requirements.txt:

```bash
pip install -r requirements.txt
```

### requirements.txt
```
numpy>=1.20.0
pandas>=1.3.0
matplotlib>=3.4.0
scipy>=1.7.0
yfinance>=0.2.0
```

## 📚 Modules

### 1. BlackScholes.py

Implements the Black-Scholes analytical formula for European options.

**Key Functions:**
- `call_option_price(S, E, T, rf, sigma)`: Calculate call option price
- `put_option_price(S, E, T, rf, sigma)`: Calculate put option price

**Parameters:**
- `S`: Current stock price
- `E`: Strike price
- `T`: Time to expiration (years)
- `rf`: Risk-free rate
- `sigma`: Volatility

**Example:**
```python
from BlackScholes import call_option_price, put_option_price

call_price = call_option_price(S0=100, E=100, T=1, rf=0.05, sigma=0.2)
put_price = put_option_price(S0=100, E=100, T=1, rf=0.05, sigma=0.2)
```

### 2. OptionPricingMonteCarlo.py & BlackScholesMonteCarlo.py

Monte Carlo simulation-based option pricing.

**Key Class:** `OptionPricing`

**Methods:**
- `call_option_simulation()`: Simulate call option price
- `put_option_simulation()`: Simulate put option price

**Example:**
```python
from OptionPricingMonteCarlo import OptionPricing

model = OptionPricing(S0=100, E=100, T=1, rf=0.05, sigma=0.2, iterations=100000)
call_value = model.call_option_simulation()
put_value = model.put_option_simulation()
```

### 3. StockPriceMonteCarlo.py

Simulates multiple stock price paths using Monte Carlo methods.

**Key Function:**
- `stock_monte_carlo(S0, mu, sigma, N)`: Generate and visualize stock price simulations

**Parameters:**
- `S0`: Initial stock price
- `mu`: Expected daily return
- `sigma`: Daily volatility
- `N`: Number of trading days (default: 252)

**Features:**
- Generates 1000 simulation paths (configurable via `NUM_OF_SIMULATIONS`)
- Plots all individual paths with transparency
- Highlights mean path in red
- Displays prediction for future stock price

**Example:**
```python
from StockPriceMonteCarlo import stock_monte_carlo

stock_monte_carlo(S0=50, mu=0.0002, sigma=0.01, N=252)
```

### 4. markowitz.py

Modern Portfolio Theory implementation for portfolio optimization.

**Key Features:**
- Downloads historical stock data from Yahoo Finance
- Generates random portfolios
- Finds optimal portfolio with maximum Sharpe ratio
- Visualizes efficient frontier

**Functions:**
- `download_data()`: Fetch stock data
- `calculate_return(data)`: Compute log returns
- `generate_portfolios(returns)`: Create random portfolio combinations
- `optimize_portfolio(weights, returns)`: Find optimal weights
- `show_optimal_portfolio()`: Visualize results

**Configuration:**
- Modify `stocks` list for different assets
- Adjust `start_date` and `end_date` for analysis period
- Change `NUM_PORTFOLIOS` for simulation count

**Output:**
- Portfolio charts saved to `results/` directory
- Summary report in `results/markowitz_summary.txt`

**Example:**
```python
# Edit the stocks list in markowitz.py
stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']

# Run the script
python markowitz.py
```

### 5. CAPM.py

Capital Asset Pricing Model for calculating beta and expected returns.

**Key Class:** `CAPM`

**Methods:**
- `download_data()`: Fetch stock and market index data
- `initialize()`: Prepare monthly returns
- `calculate_beta()`: Compute beta from covariance matrix
- `regression()`: Linear regression for alpha and beta
- `plot_regression()`: Visualize CAPM relationship

**Example:**
```python
from CAPM import CAPM

# Stock symbol and market index
capm = CAPM(['AAPL', '^GSPC'], '2018-01-01', '2023-12-31')
capm.initialize()
capm.calculate_beta()
capm.regression()
```

### 6. GBM.py

Geometric Brownian Motion simulation for stock price modeling.

**Key Functions:**
- `simulate_geometric_random_walk(S0, T, N, mu, sigma)`: Generate GBM path
- `plot_simulation(t, S)`: Visualize the process

**Parameters:**
- `S0`: Initial value
- `T`: Time horizon
- `N`: Number of time steps
- `mu`: Drift (expected return)
- `sigma`: Volatility

**Example:**
```python
from GBM import simulate_geometric_random_walk, plot_simulation

time, stock_prices = simulate_geometric_random_walk(S0=100, T=2, N=1000, mu=0.1, sigma=0.05)
plot_simulation(time, stock_prices)
```

### 7. WienerProcess.py

Standard Brownian motion (Wiener process) simulation.

**Key Functions:**
- `wiener_process(dt, x0, n)`: Generate Wiener process
- `plot_process(t, W)`: Visualize the process

**Example:**
```python
from WienerProcess import wiener_process, plot_process

time, W = wiener_process(dt=0.1, x0=0, n=1000)
plot_process(time, W)
```

### 8. TimeValueMoney.py

Time value of money calculations with different compounding methods.

**Key Functions:**
- `future_discrete_value(pv, r, t)`: Discrete compounding
- `future_continuous_value(pv, r, t)`: Continuous compounding

**Example:**
```python
from TimeValueMoney import future_discrete_value, future_continuous_value

fv_discrete = future_discrete_value(pv=1000, interest_rate=0.05, time=10)
fv_continuous = future_continuous_value(pv=1000, interest_rate=0.05, time=10)
```

### 9. zeroCouponBond.py

Zero-coupon bond valuation.

**Key Class:** `ZeroCouponBond`

**Methods:**
- `present_value(period)`: Discrete discounting
- `present_value_continuous(period)`: Continuous discounting

**Example:**
```python
from zeroCouponBond import ZeroCouponBond

bond = ZeroCouponBond(principal=1000, maturity=5, interest_rate=0.05)
pv = bond.present_value(5)
```

### 10. couponBond.py

Coupon bond valuation with periodic interest payments.

**Key Class:** `CouponBond`

**Methods:**
- `present_value(period)`: Discrete discounting
- `present_value_continuous(period)`: Continuous discounting

**Example:**
```python
from couponBond import CouponBond

bond = CouponBond(principal=1000, maturity=5, interest_rate=5, coupon_rate=6)
pv = bond.present_value(5)
```

## 💡 Usage Examples

### Example 1: Option Pricing Comparison

```python
from BlackScholes import call_option_price
from OptionPricingMonteCarlo import OptionPricing

# Parameters
S0, E, T, rf, sigma = 100, 100, 1, 0.05, 0.2

# Black-Scholes analytical price
bs_price = call_option_price(S0, E, T, rf, sigma)
print(f"Black-Scholes Call Price: ${bs_price:.2f}")

# Monte Carlo price
mc_model = OptionPricing(S0, E, T, rf, sigma, iterations=100000)
mc_price = mc_model.call_option_simulation()
print(f"Monte Carlo Call Price: ${mc_price:.2f}")
```

### Example 2: Portfolio Optimization

```python
# Edit markowitz.py to customize your portfolio
stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'JPM']
start_date = '2020-01-01'
end_date = '2023-12-31'

# Run the optimization
python markowitz.py

# Results will be saved in results/ directory:
# - optimal_portfolio.png: Efficient frontier with optimal portfolio
# - random_portfolios.png: All simulated portfolios
# - markowitz_summary.txt: Detailed optimization results
```

### Example 3: Stock Price Simulation

```python
from StockPriceMonteCarlo import stock_monte_carlo

# Simulate stock price over 1 year (252 trading days)
# Starting at $100, daily return 0.05%, daily volatility 1%
stock_monte_carlo(S0=100, mu=0.0005, sigma=0.01, N=252)

# Adjust NUM_OF_SIMULATIONS in the file to change number of paths
```

### Example 4: CAPM Analysis

```python
from CAPM import CAPM

# Analyze Apple stock vs S&P 500
capm = CAPM(['AAPL', '^GSPC'], '2020-01-01', '2023-12-31')
capm.initialize()
capm.calculate_beta()
capm.regression()

# For Indian stocks, use NSE symbols:
capm_india = CAPM(['RELIANCE.NS', '^NSEI'], '2020-01-01', '2023-12-31')
```

### Example 5: Bond Valuation

```python
from zeroCouponBond import ZeroCouponBond
from couponBond import CouponBond

# Zero-coupon bond
zcb = ZeroCouponBond(principal=1000, maturity=5, interest_rate=0.05)
print(f"Zero-Coupon Bond PV: ${zcb.present_value(5):.2f}")

# Coupon bond
cb = CouponBond(principal=1000, maturity=5, interest_rate=5, coupon_rate=6)
print(f"Coupon Bond PV: ${cb.present_value(5):.2f}")
```

## 📁 Project Structure

```
QuantFin/
│
├── BlackScholes.py                 # Black-Scholes analytical model
├── BlackScholesMonteCarlo.py       # Monte Carlo option pricing (variant)
├── OptionPricingMonteCarlo.py      # Monte Carlo option pricing
├── StockPriceMonteCarlo.py         # Stock price path simulation
├── markowitz.py                    # Portfolio optimization
├── CAPM.py                         # Capital Asset Pricing Model
├── GBM.py                          # Geometric Brownian Motion
├── WienerProcess.py                # Wiener/Brownian process
├── TimeValueMoney.py               # Time value calculations
├── zeroCouponBond.py               # Zero-coupon bond pricing
├── couponBond.py                   # Coupon bond pricing
├── README.md                       # This file
│
└── results/                        # Output directory for analysis results
    ├── markowitz_summary.txt       # Portfolio optimization summary
    ├── optimal_portfolio.png       # Optimal portfolio visualization
    ├── prices.png                  # Historical price chart
    └── random_portfolios.png       # Random portfolios scatter plot
```

## 🔧 Configuration

### Markowitz Portfolio Optimization

Edit `markowitz.py`:
```python
NUM_TRADING_DAYS = 252          # Trading days per year
NUM_PORTFOLIOS = 10000          # Number of random portfolios
stocks = ['STOCK1', 'STOCK2']   # Your stock symbols
start_date = 'YYYY-MM-DD'       # Analysis start date
end_date = 'YYYY-MM-DD'         # Analysis end date
```

### Stock Price Monte Carlo

Edit `StockPriceMonteCarlo.py`:
```python
NUM_OF_SIMULATIONS = 1000       # Number of simulation paths
```

### CAPM Analysis

Edit `CAPM.py`:
```python
RISK_FREE_RATE = 0.05           # Annual risk-free rate
MONTHS_IN_YEAR = 12             # Months for annualization
```

## 📊 Understanding the Output

### Markowitz Portfolio Optimization

The optimization generates three charts:

1. **prices.png**: Historical price movements of selected stocks
2. **random_portfolios.png**: Scatter plot of risk-return combinations (color-coded by Sharpe ratio)
3. **optimal_portfolio.png**: Same as above with green star marking the optimal portfolio

The `markowitz_summary.txt` contains:
- Annual mean returns for each stock
- Covariance matrix
- Optimal portfolio weights
- Expected return, volatility, and Sharpe ratio

### CAPM Analysis

- Beta value: Measures systematic risk relative to market
- Alpha: Regression intercept (excess return)
- Expected return: Based on CAPM formula
- Scatter plot: Shows relationship between stock and market returns

### Monte Carlo Simulations

- Multiple simulation paths visualized
- Mean path highlighted in red
- Future price prediction based on average of all paths

## 🎓 Theory Background

### Black-Scholes Model

The Black-Scholes formula for a European call option:

```
C = S₀N(d₁) - Ee^(-rT)N(d₂)

where:
d₁ = [ln(S₀/E) + (r + σ²/2)T] / (σ√T)
d₂ = d₁ - σ√T
```

### Markowitz Portfolio Theory

Optimal portfolio maximizes the Sharpe ratio:

```
Sharpe Ratio = (E[R] - Rf) / σ

where:
E[R] = Expected portfolio return
Rf = Risk-free rate
σ = Portfolio standard deviation
```

### CAPM

Expected return formula:

```
E[Rᵢ] = Rf + βᵢ(E[Rₘ] - Rf)

where:
βᵢ = Cov(Rᵢ, Rₘ) / Var(Rₘ)
```

### Geometric Brownian Motion

Stock price evolution:

```
dS = μS dt + σS dW

Solution:
S(t) = S₀ exp[(μ - σ²/2)t + σW(t)]
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: `KeyError: 'Adj Close'` or `KeyError: 'close'`
- **Solution**: The code has been updated to handle both 'Close' and 'Adj Close' columns from yfinance

**Issue**: No data downloaded for stocks
- **Solution**: Verify stock symbols are correct and date range is valid

**Issue**: Monte Carlo simulations too slow
- **Solution**: Reduce the number of iterations/simulations in the respective files

**Issue**: Plots not showing
- **Solution**: Ensure matplotlib backend is configured correctly. Add `plt.ion()` if using interactive mode

## 📝 Notes

- All stock data is fetched from Yahoo Finance using yfinance
- Indian stocks can be accessed using `.NS` suffix (e.g., 'RELIANCE.NS')
- US market index: `^GSPC` (S&P 500)
- Indian market index: `^NSEI` (Nifty 50)
- Risk-free rate typically uses US Treasury yields (e.g., 10-year T-bill)

## 🚧 Future Enhancements

Potential additions:
- American option pricing with binomial trees
- Implied volatility calculation
- Value at Risk (VaR) calculations
- Greek calculations (Delta, Gamma, Vega, Theta, Rho)
- Exotic option pricing
- Multi-factor models (Fama-French)
- Fixed income derivatives
- Credit risk models

## 📚 References

- Black, F., & Scholes, M. (1973). The Pricing of Options and Corporate Liabilities
- Markowitz, H. (1952). Portfolio Selection. The Journal of Finance
- Sharpe, W. F. (1964). Capital Asset Prices: A Theory of Market Equilibrium
- Hull, J. C. Options, Futures, and Other Derivatives

## 📄 License

This project is for educational purposes. Use at your own risk for actual trading decisions.

## 👤 Author

Created as part of quantitative finance learning and practice.

---

**Disclaimer**: This software is for educational purposes only. It should not be used for actual trading or investment decisions without proper risk management and professional advice.

