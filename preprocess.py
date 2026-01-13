import numpy as np
from sklearn.preprocessing import MinMaxScaler

def prepare(data, window=60):
    scaler = MinMaxScaler()
    data = scaler.fit_transform(data.values.reshape(-1,1))

    X, y = [], []
    for i in range(window, len(data)):
        X.append(data[i-window:i])
        y.append(data[i])

    return np.array(X), np.array(y), scaler
