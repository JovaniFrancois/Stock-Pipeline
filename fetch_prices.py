import yfinance as yf

tickers = ["AAPL", "MSFT", "NVDA", "TSLA"]
data = yf.download(tickers, period="1mo", interval="1d")
print(data.head())