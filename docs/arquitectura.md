# Arquitectura del Modelo Híbrido Super Learner

## 1. Tipo de modelo seleccionado y justificación

El modelo seleccionado corresponde a un **Super Learner** o **meta-ensamble** de aprendizaje supervisado, diseñado para series temporales univariadas semanales del precio de la caja de banano en Ecuador (2017–2025).  

El Super Learner combina los modelos base con mejor desempeño individual:

- **Ridge Regression** – Captura relaciones lineales con regularización L2.  
- **MLPRegressor (Multi-Layer Perceptron)** – Modela relaciones no lineales entre los rezagos.  
- **XGBoost** – Aprovecha la capacidad de los árboles de decisión para aprender interacciones complejas.  
- **LSTM (Long Short-Term Memory)** – Captura dependencias temporales de largo plazo mediante memoria secuencial.  

La motivación detrás del uso del Super Learner fue **integrar los puntos fuertes de cada modelo base** en un único predictor robusto, reduciendo la varianza de las predicciones individuales y mejorando la capacidad de generalización en un entorno altamente volátil como el mercado bananero.  

El meta-modelo de ensamblaje utiliza **RidgeCV** con regularización automática, lo que equilibra el peso asignado a cada modelo base mediante validación cruzada temporal (*TimeSeriesSplit*), garantizando estabilidad frente a posibles correlaciones entre las predicciones.

---

## 2. Arquitectura detallada

### 2.1. Estructura de los modelos base

| Modelo | Hiperparámetros óptimos | Características principales |
|:-------|:------------------------|:-----------------------------|
| **Ridge** | α = 1e-05 | Regularización L2, robusto ante multicolinealidad. |
| **MLPRegressor** | hidden_layer_sizes = (64,64), activation = tanh, α = 1e-06, learning_rate_init = 0.003, max_iter = 2000 | Red neuronal feed-forward con dos capas ocultas y activación *tanh*. |
| **XGBoost** | n_estimators = 300, max_depth = 3, learning_rate = 0.03, subsample = 0.8, colsample_bytree = 1.0, gamma = 0.1, reg_alpha = 0.001, reg_lambda = 1 | Ensamble de árboles con boosting secuencial, optimizado con GPU. |
| **LSTM** | n_units = 96, dropout = 0.3, lr = 0.001, batch = 16, epochs = 100 | Red recurrente secuencial con una capa LSTM y una capa densa final. |

### 2.2. Meta-modelo

- **Tipo:** RidgeCV (meta-regresor)
- **Regularización:** búsqueda automática en rango logarítmico (10⁻⁴ a 10²)
- **Entrada:** predicciones *out-of-fold (OOF)* de los cuatro modelos base
- **Salida:** precio semanal estimado (variable continua en USD)

---

## 3. Diagrama de flujo del sistema completo

![Diagrama de flujo](https://raw.githubusercontent.com/icherrez/prediccion-banano/main/images/flujo_superlearner.png)

---

## 4. Pipeline de datos (input → output)

| Etapa | Descripción | Output |
|:------|:-------------|:--------|
| **1. Carga y verificación** | Importación de datos semanales desde Excel (`precio_ecuador.xlsx`) y validación de columnas `Año`, `Semana`, `Precio`. | DataFrame estructurado. |
| **2. Feature engineering** | Generación de rezagos `Precio_t-1` a `Precio_t-5` y columna `Fecha` (lunes de cada semana). | Variables predictoras. |
| **3. Escalado** | Normalización Min-Max sobre variables explicativas (`X`). | Matrices `X_train`, `X_val`, `X_test`. |
| **4. Split temporal** | División 70 % / 15 % / 15 % (train / val / test) preservando orden cronológico. | Conjuntos segmentados. |
| **5. Entrenamiento base** | Entrenamiento de Ridge, MLP, XGBoost y LSTM con *GridSearchCV* y callbacks (EarlyStopping, ReduceLROnPlateau). | Modelos base optimizados. |
| **6. Predicciones OOF** | Validación cruzada temporal (TimeSeriesSplit) para obtener predicciones independientes. | `meta_X`, `meta_y`. |
| **7. Meta-modelado** | Entrenamiento del RidgeCV con las OOF y validación cruzada automática. | Modelo Super Learner. |
| **8. Evaluación final** | Predicción en test y cálculo de RMSE, MAE y MAPE. | Desempeño final MAPE ≈ **11.84 %**. |

---

## 5. Tecnologías y librerías utilizadas

| Categoría | Librería / Framework | Versión |
|:-----------|:--------------------|:--------|
| Lenguaje base | Python | 3.10 |
| Análisis y manipulación | `pandas`, `numpy` | 2.2.2 / 1.26.4 |
| Visualización | `matplotlib` | 3.9.1 |
| Modelado clásico | `scikit-learn` | 1.5.1 |
| Boosting | `xgboost` | 2.1.1 |
| Deep Learning | `tensorflow` | 2.17.0 |
| Entorno | Google Colab / Jupyter Notebooks | — |

El entorno se ejecuta en **CPU/GPU (CUDA)**, con compatibilidad automática para `tree_method='gpu_hist'` en XGBoost y soporte para entrenamiento acelerado en TensorFlow cuando una GPU está disponible.

---

## 6. Resultados y desempeño final

```text
=== Resultados (ordenado por MAPE) ===
Modelo     RMSE      MAE    MAPE_%
 Ridge 1.260637 1.020874 11.423158
   MLP 1.219465 1.027246 11.792251
  LSTM 1.434137 1.184895 13.579797
   XGB 1.439735 1.180436 13.720187

SuperLearner Mejorado (TEST) -> RMSE: 1.320 | MAE: 1.071 | MAPE: 11.84%

