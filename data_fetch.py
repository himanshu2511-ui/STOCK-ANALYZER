import yfinance as yf

def get_stock(symbol):
    data = yf.download(symbol, start="2018-01-01", end="2024-01-01")
    return data["Close"]

prices = get_stock("AAPL")
print(prices.tail())
