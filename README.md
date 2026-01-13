# QuantFin

A compact collection of **Python** scripts implementing common **quantitative finance** models and simulations—option pricing, stochastic processes, portfolio optimization, fixed-income pricing, and Value at Risk.

> Educational purpose ONLY.

## What’s inside

- **Option pricing** (Black–Scholes, Monte Carlo)
- **Stochastic processes** (Wiener, GBM, Ornstein–Uhlenbeck)
- **Portfolio / asset pricing** (Markowitz, CAPM)
- **Fixed income** (bond pricing, Vasicek short-rate model)
- **Risk** (parametric VaR, Monte Carlo VaR)

## Requirements

- Python **3.8+**
- Dependencies in `requirements.txt`

## Quickstart

1) Install dependencies:

```bash
pip install -r requirements.txt
```

2) Run any script directly:

```bash
python BlackScholes.py
python markowitz.py
python VaR.py
python VarMonteCarlo.py
```

Most scripts include a small configuration section near the bottom of the file (e.g., tickers, date ranges, number of simulations, confidence levels). Adjust those values for your use case.

## Project layout

All scripts live in the repository root.

Some scripts write charts and summaries under:

- `results/` (created automatically when needed)

## Scripts catalog

| Area | Script | Description |
|------|--------|-------------|
| Option pricing | `BlackScholes.py` | Analytical Black–Scholes prices for European call/put options. |
| Option pricing | `OptionPricingMonteCarlo.py` | Monte Carlo option pricing for European options. |
| Option pricing | `BlackScholesMonteCarlo.py` | Alternative Monte Carlo Black–Scholes implementation. |
| Stochastic processes | `WienerProcess.py` | Standard Brownian motion simulation. |
| Stochastic processes | `GBM.py` | Geometric Brownian Motion simulation. |
| Stochastic processes | `OrnsteinUhlenbeckProcess.py` | Ornstein–Uhlenbeck process simulation. |
| Stochastic processes | `StockPriceMonteCarlo.py` | Monte Carlo simulation of stock price paths. |
| Portfolio / asset pricing | `markowitz.py` | Markowitz portfolio optimization (random portfolios + SLSQP). Saves figures and a summary under `results/`. |
| Portfolio / asset pricing | `CAPM.py` | CAPM beta estimation and regression. |
| Fixed income | `zeroCouponBond.py` | Zero-coupon bond present value (discrete/continuous). |
| Fixed income | `couponBond.py` | Coupon bond valuation. |
| Fixed income | `VasicekModel.py` | Vasicek short-rate model simulation / helpers. |
| Fixed income | `BondPricingVasecik.py` | Vasicek-model bond pricing. |
| Time value of money | `TimeValueMoney.py` | Discrete and continuous compounding helpers. |
| Risk | `VaR.py` | Parametric (variance-covariance) VaR. |
| Risk | `VarMonteCarlo.py` | Monte Carlo VaR using a GBM return model. |

## Examples

### 1) Markowitz optimization

- Edit the tickers and date range in `markowitz.py`
- Run it:

```bash
python markowitz.py
```

Outputs are typically saved to `results/` (plots + a text/console summary, depending on the script).

### 2) Value at Risk (VaR)

- Parametric VaR:

```bash
python VaR.py
```

- Monte Carlo VaR:

```bash
python VarMonteCarlo.py
```

> Tip: Monte Carlo results vary run-to-run unless a random seed is fixed.

## Data sources

Several scripts download market data from Yahoo Finance via `yfinance`.

- US tickers: `AAPL`, `MSFT`
- Indian NSE tickers: append `.NS` (e.g., `RELIANCE.NS`)
- Indices: `^GSPC` (S&P 500), `^NSEI` (Nifty 50)

## Troubleshooting

### `KeyError: 'Close'` (or missing price column)

Yahoo Finance data can vary by ticker and by `yfinance` version. In some cases:

- The returned DataFrame may not include a `Close` column (it may use `Adj Close`).
- The returned DataFrame may have **MultiIndex columns** (e.g., `(field, ticker)`), especially when downloading multiple tickers.

This repository includes defensive price extraction logic in `VarMonteCarlo.py` and `VaR.py` that:

- prefers `Adj Close` when available
- falls back to `Close`
- supports both single-index and MultiIndex column layouts

If you add scripts that rely on Yahoo Finance prices, consider reusing the same logic.

### No data returned

- Verify the symbol exists on Yahoo Finance and the date range is valid.
- Try a shorter date range to confirm the symbol works.

## Contributing

Issues and small improvements are welcome—especially around:

- making scripts more reproducible (random seeds)
- improving error handling for data downloads
- adding unit tests for the math/finance helpers

If you plan to expand this into a reusable library, consider converting the scripts into a package structure (e.g., `src/quantfin/`) and adding a test suite.

## License

This project is licensed under the **MIT License** — see [`LICENSE`](LICENSE).
