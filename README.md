# Portfolio Optimization | Actinver Investment Challenge

## Overview

This project implements a quantitative portfolio optimization model developed for an Actinver investment challenge, using Python to analyze financial assets, estimate portfolio risk and return, and construct an optimal asset allocation under investment constraints.

The model evaluates a universe of Mexican and international equities, ETFs, fixed-income instruments, and FIBRAs using historical market data.

## Objectives

- Maximize expected annualized portfolio returns.
- Allocate 60% of capital to fixed-income instruments and 40% to variable-income assets.
- Limit individual asset exposure to 10% of total portfolio value.
- Apply an annual downside-risk constraint based on a 95% normal-approximation return quantile.
- Account for exchange-rate effects when evaluating assets in Mexican pesos.

## Methodology

**1. Data Collection and Processing**

Historical financial data is obtained using Yahoo Finance (`yfinance`) and Excel datasets. Prices are cleaned, aligned, and converted into logarithmic returns.

**2. Risk and Return Estimation**

The model estimates annualized expected returns and a covariance matrix using historical daily returns.

**3. Portfolio Optimization**

Portfolio weights are determined through constrained numerical optimization using SciPy's Sequential Least Squares Programming (SLSQP) algorithm.

**4. Risk Assessment**

The optimized portfolio is evaluated using expected annual return, annualized volatility, and a 95% downside-return threshold.

## Technologies

- Python
- pandas and NumPy
- SciPy
- yfinance
- Excel / openpyxl

## Investment Constraints

| Constraint | Specification |
|---|---|
| Fixed-income allocation | 60% |
| Variable-income allocation | 40% |
| Maximum weight per asset | 10% |
| Short selling | Not allowed |
| Downside-risk threshold | Annual 95% return quantile ≥ −2.5% |

## Running the Project

Install the dependencies listed in `requirements.txt`, configure the required historical datasets, and execute:

```bash
python Actinver.py
```

The program prints the optimized portfolio's annualized expected return, volatility, downside-risk measure, and asset weights.

## Disclaimer

This project was developed for educational and portfolio-analysis purposes. It does not constitute financial advice. Historical performance and estimated risk measures do not guarantee future investment results.