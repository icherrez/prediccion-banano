# Optimización del modelo SuperLearner

---

## 1. Proceso de optimización de hiperparámetros

El proyecto **“Optimización del modelo SuperLearner para pronóstico del precio de comercialización de banano en Ecuador”** implementó un proceso de búsqueda sistemática y análisis de sensibilidad de hiperparámetros sobre un ensamble conformado por **Ridge, MLP, XGBoost y LSTM**, integrados mediante un meta-modelo **RidgeCV**.

En la configuración inicial (Ridge α=0.4655, MLP (50,50), XGBoost lr=0.05, LSTM dropout=0.3), el SuperLearner alcanzó un **MAPE de 12.86%**.  
Tras la optimización, con **α=1e-05 (Ridge)**, **learning_rate_init=0.003 (MLP)**, **learning_rate=0.03 y max_depth=3 (XGBoost)**, **n_units=96 y dropout=0.2 (LSTM)**, el modelo logró un **MAPE de 11.42%**, mejorando en **11.2%** su desempeño.

Se probaron más de **50 combinaciones durante 50 minutos de búsqueda sistemática**, logrando un modelo más **preciso, estable y eficiente** para el análisis predictivo del sector bananero ecuatoriano.

---

## 2. Hiperparámetros explorados y rangos

| Modelo | Hiperparámetro | Rango Exploratorio |
|---------|----------------|--------------------|
| Ridge | α (regularización L2) | [1e-06, 1e+03] |
| MLP | α (L2), learning_rate_init, activation | [1e-06–1e-02], [1e-4–3e-3], {relu, tanh} |
| XGBoost | learning_rate, max_depth, subsample, gamma | [0.01–0.06], [2–5], [0.8–1.0], [0–0.1] |
| LSTM | n_units, dropout, lr, batch_size | [32–144], [0.1–0.3], [1e-3–5e-4], {16, 32} |
| Meta-modelo (RidgeCV) | α | [1e-04–1e+02] |

Los experimentos se realizaron bajo **validación cruzada temporal (TimeSeriesSplit)** con 5 divisiones, garantizando independencia entre entrenamiento y validación.

---

## 3. Resultados del análisis de sensibilidad

El parámetro **α del Ridge** fue el más sensible, mostrando una relación logarítmica entre regularización y error. En valores bajos (α ≤ 1e-3), el MAPE se mantiene estable; en valores altos, aumenta significativamente.  

El **LSTM** mostró alta dependencia de `n_units` y `dropout`, mientras que el **XGBoost** fue más estable, con una influencia notable del `learning_rate` y menor del `max_depth`.

**Figura 1.** Sensibilidad individual de hiperparámetros en los modelos base del SuperLearner (MAPE en validación).  
![Figura 1](https://github.com/icherrez/prediccion-banano/blob/main/images/sensibilidad_hiperparametros.jpeg)

| Hiperparámetro | Modelo | Nivel de Sensibilidad | Valor Actual | Valor Óptimo | Mejora Potencial (±%) |
|----------------|--------|-----------------------|---------------|---------------|------------------------|
| α (regularización L2) | Ridge | Crítico | 0.4655 | 1e-05 | ±3.0% |
| α (regularización L2) | MLP | Moderado | 1e-06 | 1e-06 | ±1.0% |
| learning_rate_init | MLP | Bajo | 0.003 | 0.003 | ±0.5% |
| learning_rate | XGBoost | Moderado | 0.03 | 0.02 | ±1.5% |
| max_depth | XGBoost | Bajo | 3 | 2 | ±0.8% |
| n_units | LSTM | Crítico | 96 | 120 | ±2.5% |
| dropout | LSTM | Moderado | 0.3 | 0.1 | ±1.5% |

---

## 4. Partial Dependence Plots

Los gráficos de dependencia parcial evidenciaron los efectos marginales de cada hiperparámetro:

- **Ridge:** el error crece exponencialmente con α.  
- **MLP:** variaciones pequeñas en α y learning_rate_init generan leves oscilaciones en el MAPE.  
- **XGBoost:** el learning_rate es más relevante que max_depth, donde valores conservadores logran la menor pérdida.  
- **LSTM:** el número de neuronas muestra efecto decreciente sobre el error hasta saturación.

Estos resultados validan la necesidad de un ajuste fino en regularización y tasa de aprendizaje, más que en arquitectura profunda.

---

## 5. Ranking de importancia de hiperparámetros

El **α del Ridge** concentró el **59% de la variabilidad total del error**, seguido por `max_depth` y `learning_rate` de XGBoost.  

**Figura 2.** Ranking de importancia de hiperparámetros en los modelos base del SuperLearner.  
![Figura 2](https://github.com/icherrez/prediccion-banano/blob/main/images/ranking_importancia.png)

| Ranking | Hiperparámetro | Importancia (%) | Clasificación | Acción Recomendada |
|----------|----------------|----------------|----------------|-------------------|
| 1 | α (regularización L2) | 58.93 | ● Crítico | Optimizar urgentemente |
| 2 | max_depth (XGBoost) | 15.23 | ● Importante/Moderado | Ajuste fino |
| 3 | learning_rate (XGBoost) | 13.72 | ● Importante/Moderado | Ajuste fino |
| 4 | learning_rate_init (MLP) | 7.61 | ● Bajo | Mantener valor actual |
| 5 | modelo_Ridge | 2.39 | ● Bajo | Mantener valor actual |
| 6 | modelo_MLP | 1.20 | ● Bajo | Mantener valor actual |
| 7 | modelo_XGB | 0.92 | ● Bajo | Mantener valor actual |

---

## 6. Análisis de interacciones

En el **MLP**, se observó una **interacción negativa** entre `α` y `learning_rate_init`: al incrementarse ambos, el error aumenta. La mejor combinación se obtuvo con α ≤ 1e-6 y lr_init ≤ 1e-4.  

En el **XGBoost**, se identificó una **interacción moderada** entre `learning_rate` y `max_depth`, con los valores óptimos lr=0.01–0.02 y depth=2–3, que mejoran la convergencia y reducen el sobreajuste.

**Figura 3.** Mapas de calor de interacción de hiperparámetros en MLP y XGBoost.  
![Figura 3](https://github.com/icherrez/prediccion-banano/blob/main/images/interacciones_heatmap.jpeg)

---

## 7. Configuración final seleccionada y justificación

| Modelo | Hiperparámetro | Valor Final | Justificación |
|---------|----------------|--------------|----------------|
| Ridge | α = 1e-05 | Reducción del MAPE en +3%, mejor generalización |
| MLP | (64,64), α=1e-06, lr_init=0.003 | Arquitectura estable con mínima pérdida |
| XGBoost | lr=0.03, max_depth=3, subsample=0.9 | Balance entre convergencia y regularización |
| LSTM | n_units=96, dropout=0.2, lr=0.001 | Mayor estabilidad y reducción de ruido |
| Meta-modelo (RidgeCV) | α adaptativo | Regularización automática vía validación cruzada |

Esta configuración consolidó un **MAPE final de 11.84%**, manteniendo un costo computacional aceptable.

---

## 8. Comparación antes / después de la optimización

| Aspecto | Configuración Original | Configuración Optimizada | Cambio |
|----------|------------------------|---------------------------|---------|
| Métrica principal (MAPE, %) | 13.48 | **11.84** | −1.64 % |
| Tiempo de entrenamiento total | 42.5 min | 48.9 min | +15.1 % |
| Tamaño promedio del modelo | 27.4 MB | 29.2 MB | +6.6 % |
| Complejidad del modelo | Media | Media–Alta | ↑ ligero incremento |



---





