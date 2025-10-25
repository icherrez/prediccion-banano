import numpy as np

def forecast_k_steps(models, scaler, last_prices, k=5):
    """
    Forecast iterativo k pasos con actualización de lags.
    models: dict con predictores {"Ridge": ..., "MLP": ..., "XGB": ..., "LSTM": ..., "SuperLearner": ...}
    scaler: MinMaxScaler ajustado a los features
    last_prices: últimas observaciones reales
    """
    out = {m: [] for m in models.keys()}
    for model_name in models.keys():
        state = list(last_prices)
        for _ in range(k):
            lags = np.array(state[-5:][::-1])
            X_feat = scaler.transform(lags.reshape(1, -1))
            if model_name == "LSTM":
                y_hat = models[model_name](X_feat.reshape(1, X_feat.shape[1], 1)).ravel()[0]
            else:
                y_hat = models[model_name].predict(X_feat)[0]
            out[model_name].append(float(y_hat))
            state.append(float(y_hat))
    return out
