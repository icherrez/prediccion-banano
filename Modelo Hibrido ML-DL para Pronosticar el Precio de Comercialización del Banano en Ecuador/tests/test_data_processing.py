# ============================================================
# Pruebas unitarias de procesamiento de datos (ligeras, sin modelos)
# Ejecuta con: pytest -q
# ============================================================

import os
import numpy as np
import pandas as pd
import pytest
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

# -----------------------------
# Utilidades bajo prueba
# -----------------------------
def make_fecha_iso(df, year_col="Año", week_col="Semana", target_col="Fecha"):
    """Crea columna Fecha a partir de Año/Semana (ISO week: %G%V%u) y ordena por fecha."""
    df = df.copy()
    df[target_col] = pd.to_datetime(
        df[year_col].astype(str) + df[week_col].astype(str) + "1",
        format="%G%V%u"
    )
    df = df.sort_values(target_col).reset_index(drop=True)
    return df

def add_lags(df, target="Precio", n_lags=5):
    """Agrega columnas Precio_t-1 ... Precio_t-n_lags y elimina filas con NaN."""
    df = df.copy()
    for i in range(1, n_lags + 1):
        df[f"{target}_t-{i}"] = df[target].shift(i)
    return df.dropna().reset_index(drop=True)

def split_temporal(X, y, train_ratio=0.70, val_ratio=0.15):
    """Divide por índices: train | val | test manteniendo el orden temporal."""
    n = len(X)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))
    X_tr, X_va, X_te = X[:train_end], X[train_end:val_end], X[val_end:]
    y_tr, y_va, y_te = y[:train_end], y[train_end:val_end], y[val_end:]
    return X_tr, X_va, X_te, y_tr, y_va, y_te

def MAPE(y_true, y_pred, eps=1e-8):
    y_true = np.array(y_true, dtype=float)
    y_pred = np.array(y_pred, dtype=float)
    denom = np.maximum(np.abs(y_true), eps)
    return np.mean(np.abs((y_true - y_pred) / denom)) * 100

def to_seq(X):
    """(n_samples, n_features) -> (n_samples, timesteps=n_features, 1)"""
    X = np.asarray(X)
    return X.reshape((X.shape[0], X.shape[1], 1))


# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture(scope="module")
def df_raw():
    """
    Intenta cargar app/assets/precio_ecuador.xlsx.
    Si no existe (p.ej. en CI), genera un dataset sintético coherente.
    """
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    demo_path = os.path.join(repo_root, "app", "assets", "precio_ecuador.xlsx")

    if os.path.exists(demo_path):
        df = pd.read_excel(demo_path)
        # Chequeo mínimo de columnas esperadas
        expected_cols = {"Año", "Semana", "Precio"}
        missing = expected_cols - set(df.columns)
        assert not missing, f"Faltan columnas en demo: {missing}"
        return df

    # ---- Fallback sintético (si no está el archivo demo) ----
    # Genera 40 semanas consecutivas en ISO a caballo de un año
    weeks = list(range(45, 53)) + list(range(1, 32))  # 8 + 31 = 39 semanas
    years = [2024] * 8 + [2025] * 31
    rng = np.random.default_rng(42)
    base_price = 1.0 + 0.01 * np.arange(len(weeks)) + rng.normal(0, 0.02, len(weeks))

    df = pd.DataFrame({"Año": years, "Semana": weeks, "Precio": np.round(base_price, 3)})
    return df


@pytest.fixture(scope="module")
def df_prepared(df_raw):
    """Aplica creación de Fecha y lags."""
    df = make_fecha_iso(df_raw)
    df = add_lags(df, target="Precio", n_lags=5)
    return df


# -----------------------------
# Tests
# -----------------------------
def test_fecha_iso_conversion_and_sort(df_raw):
    df = make_fecha_iso(df_raw)
    assert "Fecha" in df.columns
    assert np.issubdtype(df["Fecha"].dtype, np.datetime64)

    # Fechas estrictamente crecientes
    diffs = df["Fecha"].diff().dropna()
    assert (diffs.dt.days > 0).all(), "Las fechas no están estrictamente ordenadas crecientes."

def test_lags_creation(df_prepared):
    # Debe contener las columnas de lags
    for i in range(1, 6):
        assert f"Precio_t-{i}" in df_prepared.columns

    # No debe haber NaN tras dropna
    assert not df_prepared.isna().any().any()

    # El número de filas debe haber disminuido al menos 5 respecto del original con Fecha
    # (No verificamos exacto porque el df_raw puede venir ya con NaNs)
    # Aquí comprobamos que hay suficientes filas para dividir
    assert len(df_prepared) >= 20, "Muy pocas filas tras generar lags para poder testear splits."

def test_feature_and_target_split_and_scaler(df_prepared):
    features = [c for c in df_prepared.columns if c.startswith("Precio_t-")]
    target = "Precio"

    X_raw = df_prepared[features].values
    y = df_prepared[target].values

    scaler = MinMaxScaler().fit(X_raw)
    X = scaler.transform(X_raw)

    # Rango [0,1]
    assert np.isfinite(X).all()
    assert (X.min() >= 0.0 - 1e-8) and (X.max() <= 1.0 + 1e-8)

    # Split temporal 70/15/15
    X_tr, X_va, X_te, y_tr, y_va, y_te = split_temporal(X, y, 0.70, 0.15)
    n = len(X)
    assert len(X_tr) + len(X_va) + len(X_te) == n
    assert len(y_tr) + len(y_va) + len(y_te) == len(y)

    # No solapamiento (comprobación de bordes)
    assert len(X_tr) > 0 and len(X_te) > 0, "Train/Test no deberían estar vacíos."
    if len(X_va) > 0:
        assert X_tr[-1, 0] != X_va[0, 0] or len(X_tr) == 0, "Posible solapamiento Train/Val."
        assert X_va[-1, 0] != X_te[0, 0] or len(X_te) == 0, "Posible solapamiento Val/Test."

def test_to_seq_shape(df_prepared):
    features = [c for c in df_prepared.columns if c.startswith("Precio_t-")]
    X = df_prepared[features].values
    X_seq = to_seq(X)
    assert X_seq.shape == (X.shape[0], X.shape[1], 1)

def test_mape_known_values():
    y_true = np.array([100, 200, 300], dtype=float)
    y_pred = np.array([110, 190, 330], dtype=float)
    mape = MAPE(y_true, y_pred)
    # Cálculo manual: (10/100 + 10/200 + 30/300)/3 = (0.1 + 0.05 + 0.1)/3 = 0.25/3 = 0.08333 -> 8.333%
    assert abs(mape - 8.3333) < 1e-2

def test_feature_prefixes(df_prepared):
    features = [c for c in df_prepared.columns if c.startswith("Precio_t-")]
    assert len(features) == 5
    assert all(col.startswith("Precio_t-") for col in features)
