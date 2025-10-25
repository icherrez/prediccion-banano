from sklearn.linear_model import Ridge, RidgeCV
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input

def build_ridge(alpha=1e-5):
    return Ridge(alpha=alpha)

def build_mlp():
    return MLPRegressor(
        hidden_layer_sizes=(64, 64),
        activation='tanh',
        alpha=1e-6,
        learning_rate_init=0.003,
        max_iter=2000,
        random_state=42
    )

def build_xgb():
    return XGBRegressor(
        learning_rate=0.03,
        max_depth=3,
        subsample=0.8,
        colsample_bytree=1.0,
        gamma=0.1,
        n_estimators=300,
        reg_alpha=0.001,
        reg_lambda=1,
        objective='reg:squarederror',
        tree_method='gpu_hist' if tf.config.list_physical_devices('GPU') else 'hist',
        random_state=42
    )

def build_lstm(input_shape):
    model = Sequential([
        Input(shape=input_shape),
        LSTM(96, return_sequences=False),
        Dropout(0.3),
        Dense(1)
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='mse')
    return model

def build_meta_model(tscv):
    return RidgeCV(alphas=[1e-4, 1e-3, 1e-2, 0.1, 1, 10], cv=tscv)
