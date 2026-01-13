import numpy as np

def allocate(returns):
    weights = returns / returns.sum()
    return weights
