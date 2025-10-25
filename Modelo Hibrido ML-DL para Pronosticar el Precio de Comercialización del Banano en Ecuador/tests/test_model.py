# ============================================================
# Pruebas ligeras de modelos y stacking (SuperLearner)
# Ejecuta con: pytest -q
# ============================================================

import os
import numpy as np
import pytest

from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error

# XGBoost (opcional): si no está instalado, se salta esa parte
try:
    from xgboost import XGBRegressor
    HAS_XGB = True
except Exception:
    HAS_XGB = False

# TensorFlow (opcional): si no está instalado, se omite la prueba LSTM
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
    tf.get_logger().setLevel("ERROR")
    tf.keras.utils.disable_interactive_logging()
    HAS_TF = True
except Exception:
    HAS_TF = False


# -----------------------------
# Utilidades
# -----------------------------
def set_all_seeds(seed: int = 42):
    np.random.seed(seed)
    if HAS_TF:
        tf.random.set_seed(seed)

def MAPE(y_true, y_pred, eps=1e-8):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    denom = np.maximum(np.abs(y_true), eps)
    return float(np.mean(np.abs((y_true - y_pred) / denom)) * 100.0)

def to_seq(X):
    X = np.asarray(X)
    return X.reshape((X.shape[0], X.shape[1], 1))


# -----------------------------
# Fixtures: datos sintéticos y splits
# -----------------------------
@pytest.fixture(scope="module")
def toy_data():
    """
    Genera una serie temporal sintética con tendencia + estacionalidad + ruido,
    crea 5 lags, escala features y hace split 70/15/15.
    """
    set_all_seeds(42)
    n = 150
    t = np.arange(n)
    # serie sintética: tendencia suave + estacionalidad semanal + ruido
    y = 1.0 + 0.003 * t + 0.1 * np.sin(2 * np.pi * t / 12.0) + np.random.normal(0, 0.03, n)
    y = y.astype(float)

    # construir lags (5)
    def add_lags(arr, n_lags=5):
        out = []
        for i in range(n_lags, len(arr)):
            out.append(arr[i - n_lags:i][::-1])  # [t-1, ..., t-5]
        X_ = np.array(out)
        y_ = arr[n_lags:]
        return X_, y_

    X_raw, y_all = add_lags(y, n_lags=5)

    # escalar features
    scaler = MinMaxScaler().fit(X_raw)
    X = scaler.transform(X_raw)

    # split temporal 70/15/15
    n2 = len(X)
    tr_end = int(n2 * 0.70)
    va_end = int(n2 * 0.85)

    X_tr, X_va, X_te = X[:tr_end], X[tr_end:va_end], X[va_end:]
    y_tr, y_va, y_te = y_all[:tr_end], y_all[tr_end:va_end], y_all[va_end:]

    return {
        "X_tr": X_tr, "X_va": X_va, "X_te": X_te,
        "y_tr": y_tr, "y_va": y_va, "y_te": y_te,
        "scaler": scaler
    }


# -----------------------------
# Tests de modelos base
# -----------------------------
def test_ridge_and_mlp_fit_predict(toy_data):
    X_tr, X_va, X_te = toy_data["X_tr"], toy_data["X_va"], toy_data["X_te"]
    y_tr, y_va, y_te = toy_data["y_tr"], toy_data["y_va"], toy_data["y_te"]

    set_all_seeds(42)

    # Ridge (rápido)
    ridge = Ridge(alpha=1e-4)
    ridge.fit(X_tr, y_tr)
    y_pred_ridge = ridge.predict(X_te)
    assert y_pred_ridge.shape == y_te.shape
    assert np.isfinite(y_pred_ridge).all()

    # MLP ligero (capas pequeñas y pocas iteraciones)
    mlp = MLPRegressor(hidden_layer_sizes=(16, 16), alpha=1e-4,
                       learning_rate_init=0.005, max_iter=300, random_state=42)
    mlp.fit(X_tr, y_tr)
    y_pred_mlp = mlp.predict(X_te)
    assert y_pred_mlp.shape == y_te.shape
    assert np.isfinite(y_pred_mlp).all()

@pytest.mark.skipif(not HAS_XGB, reason="xgboost no está instalado en el entorno de pruebas")
def test_xgb_fit_predict(toy_data):
    X_tr, X_va, X_te = toy_data["X_tr"], toy_data["X_va"], toy_data["X_te"]
    y_tr, y_va, y_te = toy_data["y_tr"], toy_data["y_va"], toy_data["y_te"]

    set_all_seeds(42)

    # XGB compacto/rápido
    xgb = XGBRegressor(
        max_depth=2,
        learning_rate=0.08,
        n_estimators=60,
        subsample=0.9,
        colsample_bytree=1.0,
        objective="reg:squarederror",
        tree_method="hist",   # 'hist' es portable/rápido (mejor que forzar 'gpu_hist' en CI)
        random_state=42
    )
    xgb.fit(X_tr, y_tr, verbose=False)
    y_pred_xgb = xgb.predict(X_te)
    assert y_pred_xgb.shape == y_te.shape
    assert np.isfinite(y_pred_xgb).all()

@pytest.mark.skipif(not HAS_TF, reason="TensorFlow no está instalado en el entorno de pruebas")
@pytest.mark.slow
def test_lstm_fit_predict(toy_data):
    X_tr, X_va, X_te = toy_data["X_tr"], toy_data["X_va"], toy_data["X_te"]
    y_tr, y_va, y_te = toy_data["y_tr"], toy_data["y_va"], toy_data["y_te"]

    set_all_seeds(42)

    X_tr_l, X_va_l, X_te_l = to_seq(X_tr), to_seq(X_va), to_seq(X_te)

    model = Sequential([
        Input(shape=(X_tr_l.shape[1], 1)),
        LSTM(16, return_sequences=False),
        Dropout(0.1),
        Dense(1),
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.003), loss="mse")
    model.fit(X_tr_l, y_tr, validation_data=(X_va_l, y_va),
              epochs=8, batch_size=16, verbose="silent")

    y_pred_lstm = model.predict(X_te_l, verbose=0).ravel()
    assert y_pred_lstm.shape == y_te.shape
    assert np.isfinite(y_pred_lstm).all()


# -----------------------------
# Test de Stacking (SuperLearner simple)
# -----------------------------
def test_superlearner_stacking_shapes_and_finiteness(toy_data):
    """
    Entrena 2-3 modelos base rápidos sobre train, obtiene preds en val y test,
    entrena un meta-modelo Ridge sobre preds de val, y predice en test.
    Verifica shapes y finitud (no NaN/inf).
    """
    X_tr, X_va, X_te = toy_data["X_tr"], toy_data["X_va"], toy_data["X_te"]
    y_tr, y_va, y_te = toy_data["y_tr"], toy_data["y_va"], toy_data["y_te"]

    set_all_seeds(42)

    # Modelos base ligeros (si xgboost no está, usamos solo Ridge+MLP)
    base_models = []

    ridge = Ridge(alpha=1e-4)
    ridge.fit(X_tr, y_tr)
    base_models.append(("Ridge", ridge))

    mlp = MLPRegressor(hidden_layer_sizes=(16, 16), alpha=1e-4,
                       learning_rate_init=0.005, max_iter=300, random_state=42)
    mlp.fit(X_tr, y_tr)
    base_models.append(("MLP", mlp))

    if HAS_XGB:
        xgb = XGBRegressor(
            max_depth=2, learning_rate=0.08, n_estimators=60,
            subsample=0.9, colsample_bytree=1.0,
            objective="reg:squarederror", tree_method="hist",
            random_state=42
        )
        xgb.fit(X_tr, y_tr, verbose=False)
        base_models.append(("XGB", xgb))

    # Predicciones en val/test para stacking
    preds_val = []
    preds_test = []
    for name, mdl in base_models:
        preds_val.append(mdl.predict(X_va))
        preds_test.append(mdl.predict(X_te))

    meta_X_val = np.vstack(preds_val).T
    meta_X_test = np.vstack(preds_test).T

    # Meta-modelo (Ridge simple)
    meta_model = Ridge(alpha=0.01)
    meta_model.fit(meta_X_val, y_va)
    super_pred = meta_model.predict(meta_X_test)

    # Checks básicos
    assert super_pred.shape == y_te.shape
    assert np.isfinite(super_pred).all()

    # Métricas (opcionales): al menos finitas y razonables
    mape_super = MAPE(y_te, super_pred)
    mae_super = mean_absolute_error(y_te, super_pred)
    assert np.isfinite(mape_super) and np.isfinite(mae_super)

    # Comparación prudente: el SuperLearner no debería ser MUCHO peor que el mejor base
    base_mapes = [MAPE(y_te, p) for p in preds_test]
    if len(base_mapes) > 0:
        best_base = min(base_mapes)
        # permitimos hasta 25% peor que el mejor base para evitar falsos negativos en CI
        assert mape_super <= 1.25 * best_base + 1e-6
