import yfinance as yf
import psycopg2
import os

tickers = ["AAPL", "MSFT", "NVDA", "TSLA"]
data = yf.download(tickers, period="1mo", interval="1d")

conn = psycopg2.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    port=5432,
    dbname="stockdata",
    user="stockuser",
    password="stockpass"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS raw_prices (
        date DATE,
        ticker TEXT,
        close NUMERIC,
        UNIQUE (date, ticker)
    )
""")

for ticker in tickers:
    for date, row in data["Close"][ticker].dropna().items():
        cur.execute(
            """
            INSERT INTO raw_prices (date, ticker, close)
            VALUES (%s, %s, %s)
            ON CONFLICT (date, ticker)
            DO UPDATE SET close = EXCLUDED.close
            """,
            (date.date(), ticker, float(row))
        )

conn.commit()
cur.close()
conn.close()

print("Data inserted successfully.")