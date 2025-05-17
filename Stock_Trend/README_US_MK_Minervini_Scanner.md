
# 📈 US Markus Heitkoetter and Minervini Inspired Screener 

This Jupyter notebook implements a stock screening strategy based on principles from **Mark Minervini**, as discussed in [Secrets of a Stock Market Wizard](https://www.stockopedia.com/academy/articles/secrets-stock-market-wizard-minervini/).

## 🧠 Strategy Overview

This screener applies a fixed set of **technical filters** and chart analysis rules inspired by Minervini’s approach, often referred to as the **MVP (Minervini Volatility Pivot)** setup.

## 📊 Key Features

- Scans stocks based on price and volume patterns
- Implements hard-coded filters derived from Minervini's conditions:
  - Price above moving averages (50D, 150D, 200D)
  - 52-week highs breakout and volatility contraction
  - Volume behavior aligned with institutional buying
- Visual charting of qualifying stocks
- Produces a final report of qualifying symbols

## 🔧 How to Use

1. Open the notebook `Stock_Chart_MVP15_HardCode_FINAL_REPORT.ipynb` in Jupyter.
2. Run all cells sequentially.
3. Review:
   - The filtered list of stocks that meet Minervini-style conditions
   - Visual chart plots for each qualifying ticker

## 🛠 Requirements

- Python 3.7+
- `pandas`, `numpy`, `matplotlib`, `yfinance`, `ta`, `seaborn`

Install dependencies with:
```bash
pip install pandas numpy matplotlib yfinance ta seaborn
```
## Input: US_MK_Scanner
- Inspired by Stock Screener according to https://markusheitkoetter.com/ in TradingView

## 📤 Output: AI_Trading_Result

- A filtered list of Minervini selected stocks
- Line or candlestick charts for final report visualization
- Predicted up or down stock trend 

## 🧬 Strategy Inspiration

> "You want to buy when a stock is under accumulation, forming a base, and about to break out. Not after it's already run up."  
— **Mark Minervini**

> “SMART is an acronym which stands for: Specific Measurable Attractive Realistic Timeframe”
― **Markus Heitkoetter, THE COMPLETE GUIDE TO DAY TRADING**

This screener automates the MVP-style filtering logic based on historical data.

## 📬 Attribution

Inspired by the teachings of Mark Minervini. Adapted and implemented in Python for personal and educational use.
