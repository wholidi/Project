
# ⚡ PowerX Screener with LSTM & Graphs (Finnhub Data)

This notebook implements a stock scanner and trend prediction system inspired by **Markus Heitkoetter’s PowerX Strategy**, as described on [markusheitkoetter.com](https://markusheitkoetter.com/). It combines rule-based screening logic with a neural network (LSTM) to detect potential trading opportunities.

## 📚 PowerX Strategy Summary

Markus Heitkoetter's **PowerX strategy** focuses on:
- Identifying stocks with strong **uptrend potential**
- Relying on **price momentum** and **volume expansion**
- Using a combination of **MACD**, **Stochastic**, and **RSI** indicators to determine entry points
- Targeting 2:1 reward-to-risk setups

---

## 🔍 What This Notebook Does

- 🧠 **Fetches historical stock data** via the Finnhub API
- 📊 **Computes technical indicators** commonly used in PowerX:
  - Moving Averages
  - MACD
  - RSI
  - Stochastic Oscillator
- 📈 **Applies PowerX-style filters** to screen candidates
- 🔮 **Uses an LSTM model** to forecast short-term price trends
- 📉 **Plots historical charts and model predictions** for visual analysis

---

## 🔧 How to Use

1. Get your **[Finnhub API key](https://finnhub.io)**
2. Open `PowerX_Screener_Finnhub_LSTM_Graphs_report.ipynb` in Jupyter
3. Replace `"YOUR_FINNHUB_TOKEN"` with your actual API key
4. Run all cells in order:
   - Data loading
   - Indicator calculation
   - PowerX filter logic
   - LSTM model prediction
   - Graph generation

---

## 📦 Requirements

- Python 3.7+
- Libraries:
  - `pandas`, `numpy`, `matplotlib`, `ta`
  - `tensorflow`, `sklearn`, `yfinance`, `seaborn`, `requests`

Install with pip:
```bash
pip install pandas numpy matplotlib ta tensorflow scikit-learn yfinance seaborn requests
```

## Input: PowerX_Ticker_Only_Input_Template
List of Daily Stock scanner in Trading View according to Markus Heikoetter
. Market Cap >= 2 Billions USD
. Daily Volume > 1 Millions 
. Daily Price Change > -2%
. Each Company P/E ratio =< 50

---

## 📤 Output: PowerX_Daily_Dashboard_Natural_Phrasing_Combined_WithSeparateGraphs

- Filtered list of stocks matching PowerX rules
- LSTM-based trend predictions
- Graphs visualizing price action, indicators, and predictions

---

## 📬 Attribution

This notebook is inspired by **Markus Heitkoetter's PowerX strategy**, adapted into a Python-powered analysis and prediction tool.
