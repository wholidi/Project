
# 📊 US MK Scanner Report

Inspired by [Markus Heitkoetter](https://markusheitkoetter.com/) and the PowerX strategy.

This notebook implements a stock scanner that evaluates U.S. stocks based on technical conditions and strategy filters.

## 🚀 Features
- Scans U.S. stocks using historical price data
- Calculates technical indicators such as Moving Averages, RSI, MACD, etc.
- Applies Markus Heitkoetter-inspired filters for trend detection and volatility
- Outputs a report of qualifying tickers

## 🔧 How to Use
1. Open the Jupyter Notebook `US_MK_Scanner_report.ipynb`
2. Run the cells step-by-step:
   - Fetch stock data
   - Compute technical indicators
   - Filter based on defined rules
3. Review the resulting DataFrame/report for matching stocks

## 🛠 Requirements
- Python 3.7+
- `pandas`, `numpy`, `matplotlib`, `requests`, `yfinance`

Install via pip:
```bash
pip install pandas numpy matplotlib requests yfinance
```

## 📤 Output
- A filtered list of stocks meeting the criteria
- Optional: export to CSV or Excel

## 📬 Attribution
Inspired by Markus Heitkoetter’s PowerX strategy and adapted into a Python-based scanner.
