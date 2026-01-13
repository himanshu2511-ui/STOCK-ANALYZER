import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

st.set_page_config(page_title="AI Portfolio Optimizer", layout="centered")

st.title("📈 AI Stock Portfolio Optimizer")

# ----------------------------------------------------
# Stock universe (large-cap, liquid equities)
# ----------------------------------------------------
stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]

prices = {}
returns = {}

st.info("Downloading market data from Yahoo Finance…")

# ----------------------------------------------------
# Robust data ingestion layer
# ----------------------------------------------------
for ticker in stocks:
    data = yf.download(ticker, period="6mo", auto_adjust=True, progress=False)

    if data.empty:
        continue

    # Flatten if Yahoo returns multi-index
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    close_prices = data["Close"].dropna()

    if len(close_prices) < 2:
        continue

    start_price = float(close_prices.iloc[0])
    end_price = float(close_prices.iloc[-1])

    prices[ticker] = end_price
    returns[ticker] = (end_price - start_price) / start_price

# ----------------------------------------------------
# Fail-safe if no data
# ----------------------------------------------------
if not prices:
    st.error("Market data could not be retrieved. Check your internet connection.")
    st.stop()

# ----------------------------------------------------
# Build financial dataframe
# ----------------------------------------------------
df = pd.DataFrame({
    "Stock": list(prices.keys()),
    "Last Price ($)": [round(prices[s], 2) for s in prices],
    "6-Month Return (%)": [round(returns[s] * 100, 2) for s in prices]
})

# ----------------------------------------------------
# Portfolio optimization (return-weighted)
# ----------------------------------------------------
ret_vals = np.array(list(returns.values()))
ret_vals = np.maximum(ret_vals, 0)   # no short-selling

if ret_vals.sum() == 0:
    weights = np.ones(len(ret_vals)) / len(ret_vals)
else:
    weights = ret_vals / ret_vals.sum()

df["Portfolio Weight (%)"] = (weights * 100).round(2)

# ----------------------------------------------------
# Display financial table
# ----------------------------------------------------
st.subheader("📊 Market Snapshot")
st.dataframe(df, width="stretch")

# ----------------------------------------------------
# Pie chart (capital allocation)
# ----------------------------------------------------
st.subheader("💰 Optimized Capital Allocation")

pie_data = df.set_index("Stock")["Portfolio Weight (%)"]
st.pyplot(pie_data.plot(kind="pie", autopct="%1.1f%%", figsize=(6,6)).figure)

# ----------------------------------------------------
# Financial interpretation
# ----------------------------------------------------
st.success("Portfolio optimized using positive-return weighting from historical price action.")
