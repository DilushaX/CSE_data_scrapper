# Colombo Stock Exchange (CSE) Data Scraper & Explorer

A powerful and user-friendly tool to extract, analyze, and visualize Colombo Stock Exchange (CSE) stock data with technical indicators (Returns, Volatility, Moving Averages, VWAP).

## 🚀 Web UI (Streamlit Application)

To run the interactive Web UI where users can pick any company and date range:

```bash
cd CSE_data_scrapper
streamlit run app.py
```

### Features in UI:
- **Company Selector**: Choose from major CSE companies (JKH, HAYL, HHL, LLUB, COMB, SAMP, LOLC, etc.) or enter any custom ticker symbol.
- **Date Range Picker**: Quick presets (1 Month, 6 Months, 1 Year, 3 Years, 5 Years, Max) or custom Start/End dates.
- **Interactive Visualizations**: Interactive Candlestick (OHLC) chart, Volume subplots, and Moving Average overlays (SMA 7/20/50/200, VWAP).
- **Technical Indicators**: Automatically computes Returns (Change, Change %, Log Return), Volatility (Price Range, Spread %, Typical Price, ATR 14), and Moving Averages.
- **1-Click CSV Export**: Download the filtered data with all technical indicators straight to a CSV file.

## 💻 CLI Batch Scraper

To run the batch scraper for default target companies (JKH, HAYL, HHL, LLUB):

```bash
python3 scrape_cse.py
```

