# --- pages/cal_beta.py ---
import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import numpy as np
import plotly.graph_objects as go

# Streamlit page setup
st.set_page_config(page_title="Calculate Beta", page_icon="📉", layout="wide")

st.title("Calculate Beta and Expected Return (CAPM)")

# --- User Input Section (inside the main page) ---
st.subheader("Select Parameters for Analysis")

col1, col2 = st.columns([1, 1])

with col1:
    stock = st.selectbox(
        "Choose a Stock",
        options=["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM", "V", "JNJ"],
        index=4
    )

with col2:
    year = int(st.number_input("Number of Years",1,10))

st.divider()  # visual separator

# --- Date range ---
end = datetime.date.today()
start = datetime.date(end.year - year, end.month, end.day)

try:
    st.markdown(f"### Data Range: **{start} → {end}**")

    # --- Download S&P 500 data ---
    sp500_data = yf.download("^GSPC", start=start, end=end)
    if "Adj Close" in sp500_data.columns:
        sp500 = sp500_data[["Adj Close"]].rename(columns={"Adj Close": "sp500"})
    elif "Close" in sp500_data.columns:
        sp500 = sp500_data[["Close"]].rename(columns={"Close": "sp500"})
    else:
        raise KeyError("S&P 500 data missing both 'Adj Close' and 'Close' columns.")

    # --- Download stock data ---
    stock_data = yf.download(stock, start=start, end=end)
    if "Adj Close" in stock_data.columns:
        stock_prices = stock_data[["Adj Close"]].rename(columns={"Adj Close": "Stock"})
    elif "Close" in stock_data.columns:
        stock_prices = stock_data[["Close"]].rename(columns={"Close": "Stock"})
    else:
        raise KeyError(f"{stock} data missing both 'Adj Close' and 'Close' columns.")

    # --- Merge and clean ---
    df = pd.merge(stock_prices, sp500, left_index=True, right_index=True).dropna()

    # --- Calculate daily returns (decimal) ---
    df["Stock_ret"] = df["Stock"].pct_change()
    df["Market_ret"] = df["sp500"].pct_change()
    df = df.dropna()

    if df.empty:
        raise ValueError("No overlapping data for the chosen period.")

    # --- Regression to get Beta & Alpha ---
    beta, alpha = np.polyfit(df["Market_ret"], df["Stock_ret"], 1)

    # --- R-squared ---
    preds = alpha + beta * df["Market_ret"]
    ss_res = ((df["Stock_ret"] - preds) ** 2).sum()
    ss_tot = ((df["Stock_ret"] - df["Stock_ret"].mean()) ** 2).sum()
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else float("nan")

    # --- Annualize market return (geometric) ---
    mean_daily_market = df["Market_ret"].mean()
    annual_market_return = (1 + mean_daily_market) ** 252 - 1  # geometric annualization
    rf = 0.0
    expected_return = rf + beta * (annual_market_return - rf)

    # --- Header Layout: Stock | Beta | Return (Single Row) ---
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <h3 style="margin:0;">Stock: <span style="color:#00BFFF;">{stock}</span></h3>
            <h3 style="margin:0;">Beta: <span style="color:#FFD700;">{beta:.4f}</span></h3>
            <h3 style="margin:0;">Expected Annual Return: <span style="color:#90EE90;">{expected_return*100:.2f}%</span></h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Plot CAPM Scatter + Regression Line ---
    fig = go.Figure()

    # Scatter plot (convert to percent for readability)
    fig.add_trace(go.Scatter(
        x=df["Market_ret"] * 100,
        y=df["Stock_ret"] * 100,
        mode="markers",
        name="Daily Returns",
        marker=dict(size=6, color="#1f77b4")
    ))

    # Regression line
    x_vals = np.linspace((df["Market_ret"].min()) * 100, (df["Market_ret"].max()) * 100, 100)
    y_vals = (alpha + beta * (x_vals / 100)) * 100
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode="lines",
        name="Regression Line",
        line=dict(color="red", width=2)
    ))

    fig.update_layout(
        title=f"{stock} vs Market (S&P 500) — Daily Returns",
        xaxis_title="Market Returns (%)",
        yaxis_title=f"{stock} Returns (%)",
        template="plotly_dark",
        width=900,
        height=550,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Display chart
    st.plotly_chart(fig, use_container_width=True)

    # --- Metrics ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Beta", f"{beta:.4f}")
    c2.metric("R²", f"{r_squared:.4f}")
    c3.metric("Annual Market Return", f"{annual_market_return*100:.2f}%")

    # --- Interpretation ---
    if beta > 1:
        st.info(f"{stock} is **more volatile** than the market (β = {beta:.4f}).")
    elif beta < 1:
        st.info(f"{stock} is **less volatile** than the market (β = {beta:.4f}).")
    else:
        st.info(f"{stock} moves roughly **in line** with the market (β ≈ 1).")

except Exception as e:
    st.error(f" Error fetching or processing data: {e}")
