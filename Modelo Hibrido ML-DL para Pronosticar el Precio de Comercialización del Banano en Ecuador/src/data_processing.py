# src/data_processing.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def load_excel(path):
    """Carga un archivo Excel y devuelve un DataFrame ordenado por fecha ISO."""
    df = pd.read_excel(path)
    df['Fecha'] = pd.to_datetime(
        df['Año'].astype(str) + df['Semana'].astype(str) + '1',
        format='%G%V%u'
    )
    df = df.sort_values('Fecha').reset_index(drop=True)
    return df

def add_lags(df, target_col="Precio", n_lags=5):
    """Crea columnas de lags Precio_t-1...Precio_t-n."""
    for i in range(1, n_lags + 1):
        df[f"{target_col}_t-{i}"] = df[target_col].shift(i)
    return df.dropna().reset_index(drop=True)

def split_features_target(df, target_col="Precio"):
    """Devuelve X, y y un escalador MinMax ajustado."""
    features = [c for c in df.columns if c.startswith(f"{target_col}_t-")]
    X = df[features].values
    y = df[target_col].values
    scaler = MinMaxScaler().fit(X)
    X_scaled = scaler.transform(X)
    return X_scaled, y, scaler
