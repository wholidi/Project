
# 🚀 Minervini Screener – Dynamic Report (Python)

This Jupyter notebook implements a stock screening and filtering tool based on the **Mark Minervini** strategy, as explained in [Secrets of a Stock Market Wizard](https://www.stockopedia.com/academy/articles/secrets-stock-market-wizard-minervini/).

## 🧠 Minervini Strategy Summary

Mark Minervini's trading philosophy is rooted in **momentum trading** with strict **risk control**. Key ideas:
- Focus on **strong price trends** (especially breakouts)
- Filter for **fundamentally sound stocks** with **technical strength**
- Use **tight stop-losses** and **proper entry timing**
- Favor stocks near **52-week highs** with contraction patterns and volume support

---

## 📊 What This Notebook Does

- Fetches historical stock data (e.g., via Yahoo Finance or API)
- Computes key **technical indicators**:
  - Moving Averages (50D, 150D, 200D)
  - Relative Strength
  - 52-week High/Low positioning
  - Price contraction metrics
- Applies dynamic **Minervini filters** to select stocks showing ideal technical setups
- Outputs a final **report table** of qualifying tickers
- Optionally visualizes performance with charts

---

## 🔧 How to Use

1. Open `MInervini_Screener_Dynamic_Report.ipynb` in Jupyter or VS Code
2. Customize the list of stock symbols or use a full index
3. Run all cells in order:
   - Data collection
   - Feature computation
   - Screening logic
4. Examine the resulting filtered stock list

---

## 📦 Requirements

- Python 3.7+
- Libraries:
  - `pandas`, `numpy`, `yfinance`, `ta`, `matplotlib`, `seaborn`

Install with pip:
```bash
pip install pandas numpy yfinance ta matplotlib seaborn
```

---

## 📤 Output

- A filtered list of stocks passing Minervini-style technical checks
- A dynamic report that can be updated with fresh data
- Optionally: chart visualizations of candidate stocks

---

## 📬 Attribution

This screener is inspired by the work and methodology of **Mark Minervini**. The logic has been adapted into Python for analytical and educational purposes.
