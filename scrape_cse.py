import os
import ssl
import websocket
import certifi
import numpy as np
import pandas as pd
from tvDatafeed import TvDatafeed, Interval

# Configure certificates and bypass strict verification for local macOS environment
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

ssl._create_default_https_context = ssl._create_unverified_context

old_create_connection = websocket.create_connection
def new_create_connection(*args, **kwargs):
    kwargs['sslopt'] = {'cert_reqs': ssl.CERT_NONE}
    return old_create_connection(*args, **kwargs)
websocket.create_connection = new_create_connection


def add_technical_columns(df):
    """
    Computes Categories 1, 2, and 3 columns:
    1. Price Changes & Returns
    2. Volatility & Range
    3. Moving Averages / Trend Indicators
    """
    df = df.copy()
    
    # Base columns
    close = df['close']
    open_p = df['open']
    high = df['high']
    low = df['low']
    vol = df['volume']
    
    # -------------------------------------------------------------
    # Category 1: Price Changes & Returns
    # -------------------------------------------------------------
    prev_close = close.shift(1)
    df['Change'] = (close - prev_close).round(2)
    df['Change_%'] = ((df['Change'] / prev_close) * 100).round(2)
    df['Intraday_Change'] = (close - open_p).round(2)
    df['Intraday_Change_%'] = (((close - open_p) / open_p) * 100).round(2)
    df['Log_Return'] = np.log(close / prev_close).round(4)
    
    # -------------------------------------------------------------
    # Category 2: Volatility & Range
    # -------------------------------------------------------------
    df['Price_Range'] = (high - low).round(2)
    df['Spread_%'] = ((df['Price_Range'] / low) * 100).round(2)
    df['Typical_Price'] = ((high + low + close) / 3.0).round(2)
    
    # True Range & ATR_14
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    df['ATR_14'] = tr.rolling(window=14, min_periods=1).mean().round(2)
    
    # -------------------------------------------------------------
    # Category 3: Moving Averages / Trend Indicators
    # -------------------------------------------------------------
    df['SMA_7'] = close.rolling(window=7, min_periods=1).mean().round(2)
    df['SMA_20'] = close.rolling(window=20, min_periods=1).mean().round(2)
    df['SMA_50'] = close.rolling(window=50, min_periods=1).mean().round(2)
    df['SMA_200'] = close.rolling(window=200, min_periods=1).mean().round(2)
    
    df['EMA_12'] = close.ewm(span=12, adjust=False).mean().round(2)
    df['EMA_26'] = close.ewm(span=26, adjust=False).mean().round(2)
    
    # VWAP (Cumulative Volume Weighted Average Price)
    cum_vol = vol.cumsum()
    cum_vol_val = (df['Typical_Price'] * vol).cumsum()
    df['VWAP'] = (cum_vol_val / cum_vol).round(2)
    
    return df


def fetch_cse_data(ticker_symbol, start_date=None, end_date=None, interval=Interval.in_daily, n_bars=5000):
    """
    Fetches stock data for a given CSE symbol, calculates technical indicators,
    and filters by the provided date range.
    """
    # Ensure ticker format has exchange prefix or .N0000 if needed
    symbol = ticker_symbol.strip().upper()
    if not symbol.endswith('.N0000') and not symbol.endswith('.X0000') and '.' not in symbol:
        symbol = f"{symbol}.N0000"

    tv = TvDatafeed()
    df = tv.get_hist(symbol=symbol, exchange='CSELK', interval=interval, n_bars=n_bars)
    
    if df is None or df.empty:
        return None
    
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    
    # Compute technical columns
    df_enriched = add_technical_columns(df)
    
    # Filter by date range if provided
    if start_date is not None:
        start_str = pd.to_datetime(start_date).strftime('%Y-%m-%d')
        df_enriched = df_enriched[df_enriched.index >= start_str]
    if end_date is not None:
        end_str = pd.to_datetime(end_date).strftime('%Y-%m-%d')
        # Include full end date
        df_enriched = df_enriched[df_enriched.index <= f"{end_str} 23:59:59"]
    
    if df_enriched.empty:
        return pd.DataFrame()
    
    sub_df = df_enriched.copy()
    sub_df.reset_index(inplace=True)
    sub_df['Date'] = sub_df['datetime'].dt.strftime('%Y-%m-%d')
    
    # Format OHLCV
    sub_df['Open'] = sub_df['open'].round(2)
    sub_df['High'] = sub_df['high'].round(2)
    sub_df['Low'] = sub_df['low'].round(2)
    sub_df['Close'] = sub_df['close'].round(2)
    sub_df['Volume'] = sub_df['volume'].astype(int)
    sub_df['Turnover'] = (sub_df['Volume'] * sub_df['Typical_Price']).round(2)
    sub_df['Trades'] = None
    sub_df['Adjusted_Close'] = sub_df['Close']
    
    ordered_cols = [
        'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Turnover', 'Trades', 'Adjusted_Close',
        'Change', 'Change_%', 'Intraday_Change', 'Intraday_Change_%', 'Log_Return',
        'Price_Range', 'Spread_%', 'Typical_Price', 'ATR_14',
        'SMA_7', 'SMA_20', 'SMA_50', 'SMA_200', 'EMA_12', 'EMA_26', 'VWAP'
    ]
    
    # Keep only ordered_cols that exist
    available_cols = [c for c in ordered_cols if c in sub_df.columns]
    return sub_df[available_cols]


def scrape_cse_data():
    targets = {
        'JKH': ('JKH.N0000', 'John Keells Holdings PLC'),
        'HAYL': ('HAYL.N0000', 'Hayleys PLC'),
        'HHL': ('HHL.N0000', 'Hemas Holdings PLC'),
        'LLUB': ('LLUB.N0000', 'Chevron Lubricants Lanka PLC')
    }
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    for key, (ticker, company_name) in targets.items():
        print(f"Fetching actual exchange data for {company_name} ({ticker})...")
        try:
            final_df = fetch_cse_data(ticker, start_date='2014-01-01', end_date='2026-12-31')
            if final_df is None or final_df.empty:
                print(f"Warning: No data returned for {ticker}")
                continue
            
            csv_path = os.path.join(output_dir, f"{key}_2014_2026.csv")
            final_df.to_csv(csv_path, index=False)
            print(f"Successfully saved {len(final_df)} rows to {csv_path}")
            
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

if __name__ == "__main__":
    scrape_cse_data()

