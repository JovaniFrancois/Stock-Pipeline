import streamlit as st
import pandas as pd
import psycopg2

st.title("Stock Pipeline Dashboard")

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="stockdata",
    user="stockuser",
    password="stockpass"
)

query = "SELECT * FROM daily_returns ORDER BY date DESC"
df = pd.read_sql(query, conn)
conn.close()

st.subheader("Latest Prices")
latest = df.sort_values("date").groupby("ticker").tail(1)
cols = st.columns(len(latest))
for col, (_, row) in zip(cols, latest.iterrows()):
    col.metric(row["ticker"], f"${row['close']:.2f}", f"{row['daily_return']*100:.2f}%")

st.subheader("Price Trend")
pivot = df.pivot(index="date", columns="ticker", values="close").sort_index()
st.line_chart(pivot)

st.subheader("Daily Returns")
st.dataframe(df.sort_values("date", ascending=False).head(20))