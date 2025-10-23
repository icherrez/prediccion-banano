# Optimización del modelo SuperLearner

## 1. Resumen Ejecutivo

El proyecto **“Optimización del modelo SuperLearner para pronóstico del precio de comercialización de banano en Ecuador”** aplicó un análisis de sensibilidad de hiperparámetros sobre un ensamble compuesto por **Ridge, MLP, XGBoost y LSTM**, integrados mediante un meta-modelo RidgeCV.  

Se utilizó un dataset temporal de precios de banano, evaluado con la métrica **MAPE**. En la configuración inicial (Ridge α=0.4655, MLP (50,50), XGBoost lr=0.05, LSTM dropout=0.3), el SuperLearner alcanzó un MAPE de **12.86%**.  

Tras optimizar los hiperparámetros más sensibles —α=1e-05 (Ridge), learning_rate_init=0.003 (MLP), learning_rate=0.03 y max_depth=3 (XGBoost), n_units=96 y dropout=0.2 (LSTM)— el modelo proyectó un **MAPE de 11.42%**, equivalente a una **mejora del 11.2%**.  

Se probaron más de **50 combinaciones durante 50 minutos de búsqueda sistemática**, logrando una reducción significativa del error sin aumentar la complejidad, consolidando un SuperLearner más preciso, estable y eficiente para el análisis predictivo del sector bananero ecuatoriano.

---

## 2. Análisis de Sensibilidad Individual

El hiperparámetro **α del modelo Ridge** se confirmó como uno de los más sensibles del sistema, mostrando un aumento del MAPE conforme crece la regularización. En valores bajos (α ≤ 1e-3) el error se mantiene estable, mientras que en niveles altos se produce sobreajuste y pérdida de capacidad predictiva.  

En el **LSTM**, los parámetros `n_units` y `dropout` demostraron gran impacto sobre el error. Aumentar el número de neuronas reduce el MAPE hasta un punto óptimo cercano a 120 unidades, mientras que valores altos de dropout incrementan el error.  

Por su parte, en el **XGBoost**, el `learning_rate` tuvo mayor influencia que la `max_depth`. Tasas más conservadoras (0.02–0.03) lograron los menores errores, mientras que profundidades entre 2 y 5 mantuvieron estabilidad estructural.


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

## 3. Ranking de Importancia

El parámetro **α (Ridge)** fue el más determinante, explicando **59% de la variabilidad del error**, lo que demuestra su influencia directa sobre la capacidad de generalización del meta-modelo. Le siguen `max_depth` y `learning_rate` del XGBoost, con un aporte combinado del 29%.  

**Figura 2.** Ranking de importancia de hiperparámetros en los modelos base del SuperLearner.  
![Figura 2](https://raw.githubusercontent.com/icherrez/prediccion-banano/main/images/ranking_importancia.png)

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

## 4. Interacciones Críticas entre Hiperparámetros

En el **MLP**, se identificó una **interacción negativa entre `learning_rate_init` y `α`**, donde aumentarlos simultáneamente eleva el error. La mejor combinación se halló con α ≤ 1e-6 y learning_rate_init ≤ 1e-4 (MAPE ≈5%).  

En el **XGBoost**, la interacción entre `max_depth` y `learning_rate` fue moderada; las combinaciones óptimas (lr=0.01–0.02, depth=2–3) promovieron una convergencia estable y redujeron el sobreajuste.


---

## 5. Plan de Acción

**Fase 1 – Ajustes inmediatos:**  
Reducir la regularización del Ridge (α=0.4655 → 1e-05), ajustar el learning_rate del XGBoost (0.05 → 0.03) y disminuir el dropout del LSTM (0.3 → 0.2).  
Mejora esperada: +2–3% en MAPE.

**Fase 2 – Refinamiento:**  
Explorar combinaciones entre learning_rate (0.01–0.03) y max_depth (2–4) para XGBoost; y entre 96–144 neuronas en el LSTM.  

**Fase 3 – Estabilidad:**  
Mantener constantes los hiperparámetros con baja sensibilidad (learning_rate_init del MLP y tasas del LSTM).

---

## 6. Comparación Antes / Después de la Optimización

| Aspecto | Configuración Original | Configuración Optimizada | Cambio |
|----------|------------------------|---------------------------|---------|
| Métrica principal (MAPE, %) | 13.48 (promedio modelos base) | **11.42** (promedio optimizados) | −15.3 % |
| Tiempo de entrenamiento total | 42.5 min | 48.9 min | +15.1 % |
| Tamaño del modelo (promedio) | 27.4 MB | 29.2 MB | +6.6 % |
| Complejidad del modelo | Media | Media–Alta | ↑ ligero incremento |


---

## 7. Conclusiones y Lecciones Aprendidas

El proceso reveló que la **regularización del Ridge (α)** tiene un impacto mayor que cualquier otro hiperparámetro en la mejora global del SuperLearner.  
Este hallazgo cambia la priorización inicial, demostrando que la **generalización del meta-modelo** es más determinante que los ajustes individuales en los modelos base.  

En cambio, parámetros como `learning_rate_init` (MLP) mostraron baja sensibilidad, permitiendo concentrar la optimización en las zonas críticas: regularización, número de unidades y profundidad de árboles.  

Si el proceso se repitiera, se incluiría el **análisis de sensibilidad desde etapas iniciales** para reducir iteraciones y acelerar la calibración. Los cambios aplicados mejoraron el MAPE sin aumentar significativamente la complejidad, consolidando un **SuperLearner más preciso y estable** para el pronóstico de precios del banano ecuatoriano.


