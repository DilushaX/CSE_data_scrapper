import os
import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from scrape_cse import fetch_cse_data

# Page configuration
st.set_page_config(
    page_title="CSE Stock Data Scraper & Explorer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }
    .main-header {
        background: linear-gradient(135deg, #0d324d 0%, #7f5a83 100%);
        padding: 20px 25px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
    }
    .main-header p {
        margin: 5px 0 0 0;
        color: #e0e0e0;
        font-size: 0.95rem;
    }
    .badge {
        display: inline-block;
        background-color: rgba(255, 255, 255, 0.2);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 8px;
    }
    .stDownloadButton button {
        background-color: #2e7d32 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# List of popular CSE stocks
POPULAR_STOCKS = {
    "JKH": {"name": "John Keells Holdings PLC", "symbol": "JKH.N0000"},
    "HAYL": {"name": "Hayleys PLC", "symbol": "HAYL.N0000"},
    "HHL": {"name": "Hemas Holdings PLC", "symbol": "HHL.N0000"},
    "LLUB": {"name": "Chevron Lubricants Lanka PLC", "symbol": "LLUB.N0000"},
    "COMB": {"name": "Commercial Bank of Ceylon PLC", "symbol": "COMB.N0000"},
    "SAMP": {"name": "Sampath Bank PLC", "symbol": "SAMP.N0000"},
    "HNB": {"name": "Hatton National Bank PLC", "symbol": "HNB.N0000"},
    "DIAL": {"name": "Dialog Axiata PLC", "symbol": "DIAL.N0000"},
    "CTC": {"name": "Ceylon Tobacco Company PLC", "symbol": "CTC.N0000"},
    "MELS": {"name": "Melstacorp PLC", "symbol": "MELS.N0000"},
    "RCL": {"name": "Royal Ceramics Lanka PLC", "symbol": "RCL.N0000"},
    "BIL": {"name": "Browns Investments PLC", "symbol": "BIL.N0000"},
    "LOLC": {"name": "LOLC Holdings PLC", "symbol": "LOLC.N0000"},
    "CARG": {"name": "Cargills (Ceylon) PLC", "symbol": "CARG.N0000"},
    "ACL": {"name": "ACL Cables PLC", "symbol": "ACL.N0000"},
    "EXPO": {"name": "Expolanka Holdings PLC", "symbol": "EXPO.N0000"},
    "LFIN": {"name": "LB Finance PLC", "symbol": "LFIN.N0000"},
    "VONE": {"name": "Vallibel One PLC", "symbol": "VONE.N0000"},
    "SUN": {"name": "Sunshine Holdings PLC", "symbol": "SUN.N0000"},
    "KHL": {"name": "Keells Hotels PLC", "symbol": "KHL.N0000"},
    "DIST": {"name": "Distilleries Company of Sri Lanka PLC", "symbol": "DIST.N0000"},
    "NDB": {"name": "National Development Bank PLC", "symbol": "NDB.N0000"},
    "SEYB": {"name": "Seylan Bank PLC", "symbol": "SEYB.N0000"},
    "NTB": {"name": "Nations Trust Bank PLC", "symbol": "NTB.N0000"},
    "TKYO": {"name": "Tokyo Cement Company (Lanka) PLC", "symbol": "TKYO.N0000"},
    "DIPD": {"name": "Dipped Products PLC", "symbol": "DIPD.N0000"},
    "RICH": {"name": "Richard Pieris and Company PLC", "symbol": "RICH.N0000"},
    "AURA": {"name": "Alumex PLC", "symbol": "AURA.N0000"},
}

# Cached data fetcher
@st.cache_data(ttl=600, show_spinner=False)
def get_stock_data(symbol, start_date, end_date):
    return fetch_cse_data(symbol, start_date=start_date, end_date=end_date, n_bars=5000)

# Sidebar: Controls
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/6/6f/Colombo_Stock_Exchange_logo.svg/320px-Colombo_Stock_Exchange_logo.svg.png", width=180)
    st.markdown("### ⚙️ දත්ත තෝරාගැනීම (Settings)")
    
    # 1. Company Selection
    st.markdown("#### 1. සමාගම තෝරන්න (Select Company)")
    stock_options = [f"{k} - {v['name']}" for k, v in POPULAR_STOCKS.items()]
    stock_options.append("➕ Other / වෙනත් Ticker එකක්...")
    
    selected_option = st.selectbox(
        "Company / Ticker:",
        options=stock_options,
        index=0,
        help="Select a company from the CSE list or choose 'Other' to type a custom symbol."
    )
    
    if "Other" in selected_option:
        custom_input = st.text_input(
            "Enter CSE Ticker Symbol:",
            value="LOFC",
            help="E.g. LOFC or LOFC.N0000"
        ).strip().upper()
        
        target_symbol = custom_input if custom_input.endswith('.N0000') or '.' in custom_input else f"{custom_input}.N0000"
        company_display = f"{custom_input} (Custom Ticker)"
        raw_key = custom_input.split('.')[0]
    else:
        raw_key = selected_option.split(" - ")[0]
        target_symbol = POPULAR_STOCKS[raw_key]["symbol"]
        company_display = POPULAR_STOCKS[raw_key]["name"]

    st.markdown("---")
    
    # 2. Date Range Selection
    st.markdown("#### 2. දින පරාසය (Date Range)")
    
    today = datetime.date.today()
    preset_choice = st.radio(
        "පෙරසැකසුම් (Presets):",
        options=[
            "1 Month (මාස 1)",
            "6 Months (මාස 6)",
            "1 Year (වසර 1)",
            "3 Years (වසර 3)",
            "5 Years (වසර 5)",
            "Max (2014 - Present)",
            "Custom Range (අභිරුචි)"
        ],
        index=2
    )
    
    if preset_choice.startswith("1 Month"):
        default_start = today - datetime.timedelta(days=30)
    elif preset_choice.startswith("6 Months"):
        default_start = today - datetime.timedelta(days=180)
    elif preset_choice.startswith("1 Year"):
        default_start = today - datetime.timedelta(days=365)
    elif preset_choice.startswith("3 Years"):
        default_start = today - datetime.timedelta(days=365 * 3)
    elif preset_choice.startswith("5 Years"):
        default_start = today - datetime.timedelta(days=365 * 5)
    elif preset_choice.startswith("Max"):
        default_start = datetime.date(2014, 1, 1)
    else:
        default_start = today - datetime.timedelta(days=365)
        
    start_date = st.date_input("ආරම්භක දිනය (Start Date):", value=default_start, min_value=datetime.date(2010, 1, 1), max_value=today)
    end_date = st.date_input("අවසාන දිනය (End Date):", value=today, min_value=datetime.date(2010, 1, 1), max_value=today)
    
    if start_date > end_date:
        st.error("Error: Start Date must be before End Date!")

    st.markdown("---")
    
    # 3. Chart Options
    st.markdown("#### 3. ප්‍රස්තාර විකල්ප (Chart Overlays)")
    show_candlestick = st.checkbox("Show Candlestick (ජපන් ඉටිපන්දම් ප්‍රස්තාරය)", value=True)
    show_volume = st.checkbox("Show Volume (වෙළඳ පරිමාව)", value=True)
    show_sma = st.multiselect("Moving Averages (SMA):", options=["SMA_7", "SMA_20", "SMA_50", "SMA_200"], default=["SMA_20", "SMA_50"])
    show_vwap = st.checkbox("Show VWAP", value=False)
    
    fetch_btn = st.button("🔄 දත්ත යාවත්කාලීන කරන්න (Fetch Data)", use_container_width=True, type="primary")

# Main Page Header
st.markdown(f"""
<div class="main-header">
    <h1>🏛️ Colombo Stock Exchange (CSE) Data Scraper</h1>
    <p>ශ්‍රී ලංකා කොටස් වෙළඳපොළේ දත්ත විශ්ලේෂණය සහ බාගත කිරීමේ පද්ධතිය</p>
    <span class="badge">Selected: {company_display} ({target_symbol})</span>
    <span class="badge" style="margin-left: 8px;">Date: {start_date} to {end_date}</span>
</div>
""", unsafe_allow_html=True)

# Fetching Data
with st.spinner(f"Fetching data for {company_display} ({target_symbol})..."):
    df = get_stock_data(target_symbol, start_date=start_date, end_date=end_date)

if df is None or df.empty:
    st.warning(f"⚠️ No stock trading data found for '{target_symbol}' between {start_date} and {end_date}. Please verify the symbol or try a broader date range.")
else:
    # 1. Summary Cards
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2] if len(df) > 1 else last_row
    
    curr_close = last_row['Close']
    change_val = last_row['Change']
    change_pct = last_row['Change_%']
    high_period = df['High'].max()
    low_period = df['Low'].min()
    tot_volume = df['Volume'].sum()
    avg_atr = df['ATR_14'].dropna().iloc[-1] if 'ATR_14' in df and not df['ATR_14'].dropna().empty else 0.0

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Latest Close (රු.)", f"LKR {curr_close:,.2f}", f"{change_val:+.2f} ({change_pct:+.2f}%)")
    col2.metric("Period High (උපරිම)", f"LKR {high_period:,.2f}")
    col3.metric("Period Low (අවම)", f"LKR {low_period:,.2f}")
    col4.metric("Total Volume (පරිමාව)", f"{tot_volume:,}")
    col5.metric("Volatility (ATR 14)", f"LKR {avg_atr:,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Interactive Charts (Plotly)
    st.subheader("📈 මිල ප්‍රස්ථාරය සහ දර්ශක (Price Chart & Indicators)")
    
    rows_needed = 2 if show_volume else 1
    row_heights = [0.75, 0.25] if show_volume else [1.0]
    
    fig = make_subplots(
        rows=rows_needed,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        subplot_titles=(f"{company_display} - Price Trend", "Volume" if show_volume else ""),
        row_heights=row_heights
    )
    
    # Candlestick or Line
    if show_candlestick:
        fig.add_trace(
            go.Candlestick(
                x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name="OHLC",
                increasing_line_color='#26a69a',
                decreasing_line_color='#ef5350'
            ),
            row=1, col=1
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['Close'],
                mode='lines',
                line=dict(color='#1e88e5', width=2),
                name="Close Price"
            ),
            row=1, col=1
        )
    
    # Overlays: SMA
    colors = {'SMA_7': '#ffb300', 'SMA_20': '#f4511e', 'SMA_50': '#8e24aa', 'SMA_200': '#3949ab'}
    for ma in show_sma:
        if ma in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df[ma],
                    mode='lines',
                    line=dict(width=1.5, color=colors.get(ma, '#90a4ae')),
                    name=ma
                ),
                row=1, col=1
            )
            
    if show_vwap and 'VWAP' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['VWAP'],
                mode='lines',
                line=dict(width=1.8, dash='dot', color='#00897b'),
                name="VWAP"
            ),
            row=1, col=1
        )

    # Volume Subplot
    if show_volume:
        vol_colors = ['#26a69a' if c >= o else '#ef5350' for c, o in zip(df['Close'], df['Open'])]
        fig.add_trace(
            go.Bar(
                x=df['Date'],
                y=df['Volume'],
                marker_color=vol_colors,
                name="Volume",
                opacity=0.7
            ),
            row=2, col=1
        )
        
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        height=580,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified',
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # 3. Data Tables & Categorized Indicators
    st.markdown("---")
    st.subheader("📋 තාක්ෂණික දර්ශක සහ දත්ත සටහන (Technical Data Table)")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 සියලු දත්ත (All Columns)",
        "💰 මිල වෙනස්වීම් (Returns & Price Changes)",
        "⚡ උච්චාවචනය (Volatility & Range)",
        "📈 ප්‍රවණතා (Moving Averages)"
    ])

    with tab1:
        st.dataframe(df, use_container_width=True, height=350)
        
    with tab2:
        ret_cols = ['Date', 'Close', 'Change', 'Change_%', 'Intraday_Change', 'Intraday_Change_%', 'Log_Return']
        available_ret = [c for c in ret_cols if c in df.columns]
        st.dataframe(df[available_ret], use_container_width=True, height=350)
        
    with tab3:
        vol_cols = ['Date', 'Close', 'Price_Range', 'Spread_%', 'Typical_Price', 'ATR_14']
        available_vol = [c for c in vol_cols if c in df.columns]
        st.dataframe(df[available_vol], use_container_width=True, height=350)
        
    with tab4:
        trend_cols = ['Date', 'Close', 'SMA_7', 'SMA_20', 'SMA_50', 'SMA_200', 'EMA_12', 'EMA_26', 'VWAP']
        available_trend = [c for c in trend_cols if c in df.columns]
        st.dataframe(df[available_trend], use_container_width=True, height=350)

    # 4. Download / Export Section
    st.markdown("---")
    col_dl1, col_dl2 = st.columns([2, 1])
    with col_dl1:
        st.markdown(f"**ලබාගත් වාර්තා ගණන (Total Trading Days):** `{len(df)} records`")
        csv_data = df.to_csv(index=False).encode('utf-8')
        file_name = f"{raw_key}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
        
        st.download_button(
            label=f"📥 Download CSV Data ({file_name})",
            data=csv_data,
            file_name=file_name,
            mime="text/csv",
            key="download_csv"
        )
    with col_dl2:
        st.info("💡 **Tip:** CSV එක බාගත කර Excel, Python, හෝ R මඟින් වැඩිදුර විශ්ලේෂණය සඳහා භාවිතා කළ හැක.")
