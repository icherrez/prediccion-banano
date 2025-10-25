# src/train.py
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from src.model import build_ridge, build_mlp, build_xgb, build_lstm, build_meta_model

def to_seq(X):
    """Convierte X a formato (samples, timesteps, 1) para LSTM."""
    return X.reshape((X.shape[0], X.shape[1], 1))

def train_models(X, y, ventana_prog=None):
    """Entrena modelos base + meta-modelo con validación temporal."""
    tscv = TimeSeriesSplit(n_splits=5)
    oof_preds, oof_y = [], []

    for fold, (tr_idx, va_idx) in enumerate(tscv.split(X)):
        if ventana_prog:
            ventana_prog.agregar_texto(f"🍌 Fold {fold+1}/5: entrenamiento en curso...")

        X_tr, X_va = X[tr_idx], X[va_idx]
        y_tr, y_va = y[tr_idx], y[va_idx]

        ridge = build_ridge()
        mlp = build_mlp()
        xgb = build_xgb()
        lstm = build_lstm((X.shape[1], 1))

        ridge.fit(X_tr, y_tr)
        mlp.fit(X_tr, y_tr)
        xgb.fit(X_tr, y_tr)
        lstm.fit(to_seq(X_tr), y_tr, epochs=50, batch_size=16, verbose=0,
                 validation_data=(to_seq(X_va), y_va))

        preds = np.vstack([
            ridge.predict(X_va),
            mlp.predict(X_va),
            xgb.predict(X_va),
            lstm.predict(to_seq(X_va), verbose=0).ravel()
        ]).T

        oof_preds.append(preds)
        oof_y.append(y_va)

    meta_X = np.vstack(oof_preds)
    meta_y = np.concatenate(oof_y)

    meta_model = build_meta_model(tscv)
    meta_model.fit(meta_X, meta_y)

    return ridge, mlp, xgb, lstm, meta_model
