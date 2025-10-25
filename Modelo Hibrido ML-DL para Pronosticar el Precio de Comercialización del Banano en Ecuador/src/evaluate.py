# src/evaluate.py
import numpy as np
from math import sqrt
from sklearn.metrics import mean_squared_error, mean_absolute_error

def MAPE(y_true, y_pred, eps=1e-8):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    denom = np.maximum(np.abs(y_true), eps)
    return np.mean(np.abs((y_true - y_pred) / denom)) * 100

def report_model(y_true, y_pred, tag="Modelo"):
    rmse = sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    mape = MAPE(y_true, y_pred)
    print(f"{tag} -> RMSE: {rmse:.3f} | MAE: {mae:.3f} | MAPE: {mape:.2f}%")
    return rmse, mae, mape
