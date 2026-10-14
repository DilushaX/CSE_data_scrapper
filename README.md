# Colombo Stock Exchange (CSE) Data Scraper & Explorer

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Visualizations](https://img.shields.io/badge/Charts-Plotly-3F4F75.svg)](https://plotly.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An interactive, high-performance data scraper, technical indicator engine, and visualization dashboard tailored for the **Colombo Stock Exchange (CSE)** in Sri Lanka. 

Users can effortlessly select any listed company, customize historical date ranges, inspect technical indicators, interact with candlestick charts, and export clean datasets directly to CSV.

---

## 🌟 Key Features

- **Intuitive Company Selection**:
  - Pre-configured shortcuts for 25+ top CSE equities (John Keells Holdings, Hayleys, Hemas, Chevron Lubricants, Commercial Bank, Sampath Bank, Dialog, LOLC, etc.).
  - **Custom Ticker Support**: Search any CSE ticker directly (e.g., `LOFC`, `TKYO.N0000`, `DIPD.N0000`).
- **Flexible Date Range & Presets**:
  - Quick 1-click presets: `1 Month`, `6 Months`, `1 Year`, `3 Years`, `5 Years`, and `Max (2014 - Present)`.
  - Date picker to isolate any historical period.
- **Interactive Visualizations (Plotly)**:
  - Interactive **Candlestick (OHLC)** charts and Volume bars with hover inspection and pan/zoom.
  - Optional moving average overlays: **SMA (7, 20, 50, 200)**, **EMA (12, 26)**, and **VWAP**.
- **Comprehensive Technical Indicators**:
  - **Price Changes & Returns**: Daily Change, Percentage Change, Intraday Change, Intraday Change %, Logarithmic Return.
  - **Volatility & Range**: Daily Price Range, Spread %, Typical Price, 14-period Average True Range (`ATR_14`).
  - **Moving Averages & Trend**: Simple Moving Averages (`SMA_7`, `SMA_20`, `SMA_50`, `SMA_200`), Exponential Moving Averages (`EMA_12`, `EMA_26`), and Volume Weighted Average Price (`VWAP`).
- **1-Click CSV Export**:
  - Download all structured data including indicators with descriptive file names for quantitative research, backtesting, or spreadsheet analysis.

---

## 📁 Repository Structure

```
CSE_data_scrapper/
├── app.py              # Streamlit interactive web dashboard
├── scrape_cse.py       # Core data scraper & indicator computation engine
├── requirements.txt    # Project dependencies
├── .gitignore          # Git exclusion rules
└── README.md           # Documentation
```

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/CSE_data_scrapper.git
cd CSE_data_scrapper
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Option 1: Launch the Interactive Web Dashboard

To start the interactive UI application:

```bash
streamlit run app.py
```

Open your web browser and navigate to:
```
http://localhost:8501
```

1. Use the left sidebar to pick a **Company** or type a custom ticker symbol.
2. Select your desired **Date Range** (or click a quick preset like `1 Year`).
3. Toggle chart overlays (Candlestick, Volume, SMAs, VWAP).
4. Review metrics and categorized technical data tables.
5. Click **Download CSV Data** to export the dataset.

---

### Option 2: Run the CLI Batch Scraper

If you prefer to run a headless background scraper that extracts historical records for key targets (`JKH`, `HAYL`, `HHL`, `LLUB`) from 2014 to present:

```bash
python3 scrape_cse.py
```

The script will fetch the exchange data, compute all technical indicators, and save formatted CSV files directly into the directory.

---

## 📊 Output Column Reference

| Column | Category | Description |
|---|---|---|
| `Date` | Base | Trading day (`YYYY-MM-DD`) |
| `Open`, `High`, `Low`, `Close` | Base | OHLC exchange prices in LKR |
| `Volume` | Base | Total share volume traded |
| `Turnover` | Base | Estimated turnover value (`Volume * Typical_Price`) |
| `Adjusted_Close` | Base | Adjusted price |
| `Change` | Returns | Difference from previous close (`Close - Prev_Close`) |
| `Change_%` | Returns | Daily percentage change |
| `Intraday_Change` | Returns | Day session change (`Close - Open`) |
| `Intraday_Change_%` | Returns | Day session percentage change |
| `Log_Return` | Returns | Continuously compounded return `ln(Close / Prev_Close)` |
| `Price_Range` | Volatility | High minus Low |
| `Spread_%` | Volatility | Price range relative to low `((High - Low) / Low) * 100` |
| `Typical_Price` | Volatility | Arithmetic mean of `(High + Low + Close) / 3` |
| `ATR_14` | Volatility | 14-period Average True Range |
| `SMA_7`, `SMA_20`, `SMA_50`, `SMA_200` | Trend | Simple Moving Averages over 7, 20, 50, and 200 trading days |
| `EMA_12`, `EMA_26` | Trend | Exponential Moving Averages over 12 and 26 periods |
| `VWAP` | Trend | Cumulative Volume Weighted Average Price |

---

## 💡 Notes on Colombo Stock Exchange Tickers

CSE stocks on TradingView/tvDatafeed utilize the `CSELK` exchange code with standard ticker formats:
- Voting shares typically end in `.N0000` (e.g., `JKH.N0000`, `COMB.N0000`).
- Non-voting shares typically end in `.X0000` (e.g., `COMB.X0000`).
- If you enter a base symbol such as `JKH` in the custom ticker field, the app automatically maps it to `JKH.N0000`.

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
