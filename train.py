import yfinance as yf
from preprocess import prepare
from model import build_model

data = yf.download("AAPL", start="2018-01-01")["Close"]
X, y, scaler = prepare(data)

model = build_model()
model.fit(X, y, epochs=10, batch_size=32)

prediction = model.predict(X[-1].reshape(1,60,1))
price = scaler.inverse_transform(prediction)

print("Tomorrow Price:", price)
