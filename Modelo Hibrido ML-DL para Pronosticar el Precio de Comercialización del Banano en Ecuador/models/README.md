# Modelos entrenados – Proyecto de Predicción de Precios de Banano

Esta carpeta contiene las versiones guardadas del **SuperLearner** desarrollado para la predicción semanal del precio del banano.  
Cada versión incluye los modelos base (`Ridge`, `MLP`, `XGB`, `LSTM`) y un meta‐modelo (`Ridge` o `RidgeCV`) entrenado en diferentes etapas del proyecto.

---

## Estructura

| Archivo | Descripción | Fecha / Origen |
|----------|--------------|----------------|
| **best_model.pkl** | Versión más reciente y optimizada del ensemble. Entrenado con todo el histórico disponible usando validación temporal (`TimeSeriesSplit`, 5 folds) y `RidgeCV` como meta‐modelo con regularización automática. | Última actualización: *YYYY-MM-DD* |
| **model_v1.pkl** | Versión inicial del SuperLearner entrenada con un único split `Train/Val/Test`. Usa `Ridge(alpha=0.01)` como meta‐modelo. Mantenida para reproducibilidad y comparaciones históricas. | Entrenamiento original: *YYYY-MM-DD* |

---

## Contenido de cada `.pkl`

Cada archivo contiene un diccionario `bundle` con los siguientes elementos:

```python
{
  "ridge": <sklearn.linear_model.Ridge>,
  "mlp": <sklearn.neural_network.MLPRegressor>,
  "xgb": <xgboost.XGBRegressor>,
  "lstm": <tensorflow.keras.Sequential>,
  "meta_model": <sklearn.linear_model.Ridge or RidgeCV>,
  "scaler": <sklearn.preprocessing.MinMaxScaler> or None,
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "notes": "Descripción del conjunto y metodología"
}

