# Análisis de Datos

## 1. Descripción detallada del dataset

El conjunto de datos fue proporcionado por el **Observatorio Estadístico de Banano** y contiene información **semanal desde 2017 hasta 2025**, recopilada a partir de un panel de **10 productores y 10 exportadores** del sector bananero.  
Su acceso es restringido a suscriptores a través del portal [observatoriobanano.com/precios](https://observatoriobanano.com/precios).  

- **Número total de registros:** 453  
- **Variables:**  
  - `Año` *(int64)*  
  - `Semana` *(int64)*  
  - `Precio` *(float64)*  
- **Rango temporal:** 2017–2025  
- **Frecuencia:** Semanal  
- **Tamaño en memoria:** 10.7 KB  

La serie está completa, ordenada cronológicamente y sin valores nulos ni duplicados, lo que garantiza su integridad para modelado predictivo.

---

## 2. Estadísticas descriptivas

| Medida | Precio (USD/caja) |
|:-------|:-----------------:|
| Recuento | 453 |
| Media | 6.83 |
| Desviación estándar | 2.61 |
| Mínimo | 1.80 |
| Percentil 25% | 4.98 |
| Mediana | 6.50 |
| Percentil 75% | 8.41 |
| Máximo | 15.00 |

El precio promedio fue **6.83 USD**, con una **mediana de 6.50 USD**, evidenciando un sesgo positivo causado por valores altos atípicos.  
La **desviación estándar (2.61)** y el **coeficiente de variación (38.14%)** reflejan la alta volatilidad del mercado bananero.  
La **prueba de Shapiro-Wilk** (p = 0.000) confirma que la distribución **no es normal** y presenta ligera asimetría positiva.

---

## 3. Visualizaciones del EDA

A continuación se listan las visualizaciones clave generadas:

1. **Histograma de distribución de precios**  
![Histograma de precios](https://raw.githubusercontent.com/icherrez/prediccion-banano/blob/main/Modelo%20Hibrido%20ML-DL%20para%20Pronosticar%20el%20Precio%20de%20Comercialización%20del%20Banano%20en%20Ecuador/images/histograma_precios.png)

2. **Boxplot de precios con outliers**  
![Boxplot de precios](https://raw.githubusercontent.com/icherrez/prediccion-banano/blob/main/Modelo%20Hibrido%20ML-DL%20para%20Pronosticar%20el%20Precio%20de%20Comercialización%20del%20Banano%20en%20Ecuador/images/boxplot_precios.png)

3. **Serie temporal con outliers detectados por Z-score e IQR**  
![Serie temporal con outliers](https://raw.githubusercontent.com/icherrez/prediccion-banano/blob/main/Modelo%20Hibrido%20ML-DL%20para%20Pronosticar%20el%20Precio%20de%20Comercialización%20del%20Banano%20en%20Ecuador/images/serie_outliers.png)

4. **Comparativo serie original vs procesada (winsorizing)**  
![Serie original vs procesada (winsorizing)](https://raw.githubusercontent.com/icherrez/prediccion-banano/blob/main/Modelo%20Hibrido%20ML-DL%20para%20Pronosticar%20el%20Precio%20de%20Comercialización%20del%20Banano%20en%20Ecuador/images/serie_winsorizing.png)

5. **Boxplot comparativo antes y después del tratamiento**  
![Boxplot comparativo original vs procesada](https://raw.githubusercontent.com/icherrez/prediccion-banano/blob/main/Modelo%20Hibrido%20ML-DL%20para%20Pronosticar%20el%20Precio%20de%20Comercialización%20del%20Banano%20en%20Ecuador/images/boxplot_comparativo.png)

6. **Descomposición STL (tendencia, estacionalidad y residuo)**  
![Descomposición STL](https://raw.githubusercontent.com/icherrez/prediccion-banano/blob/main/Modelo%20Hibrido%20ML-DL%20para%20Pronosticar%20el%20Precio%20de%20Comercialización%20del%20Banano%20en%20Ecuador/images/stl_descomposicion.png)

Estas visualizaciones muestran la concentración de precios entre 6 y 8 USD, valores extremos en 2018 y una tendencia ascendente posterior a 2022.

---

## 4. Identificación de patrones, correlaciones y outliers

El análisis exploratorio reveló:

- **Patrón temporal:** tendencia estable hasta 2021 y ascendente desde 2022.  
- **Estacionalidad:** ciclos anuales recurrentes en el precio semanal.  
- **Outliers:** identificados mediante Z-score (> 3 σ) y método IQR, concentrados entre 2017–2018 con valores > 14 USD.  
- **Correlaciones:** las pruebas con variables exógenas (producción, exportaciones, precios internacionales) no mejoraron el rendimiento, confirmando la superioridad del enfoque **univariado autoregresivo** (precio con rezagos).  

Conclusión: la información relevante para el pronóstico se concentra en la dinámica interna del precio, sin aportes significativos de variables externas en el horizonte semanal.

---

## 5. Decisiones de preprocesamiento justificadas

Las decisiones clave fueron:

1. **Interpolación lineal (preventiva):** incluida en el pipeline aunque no existan valores nulos, para mantener consistencia en futuras actualizaciones.  
2. **Winsorizing (1% en extremos):** suaviza la influencia de picos anómalos manteniendo la información histórica.  
3. **Generación de rezagos (lags 1–5):** captura dependencias temporales entre semanas, clave en el modelo autoregresivo.  
4. **Escalado Min-Max (0–1):** esencial para algoritmos sensibles a magnitudes (redes neuronales, SVR, ensambles).  
5. **Partición temporal 70/15/15:** respeta la cronología y evita *data leakage*.
6. Al ser datos históricos, se decidido usar la serie original dado la baja influencia de los outliers.


Pipeline resumido:

```python
pipeline = Pipeline([
    ("interpolacion", Interpolator()),
    ("winsorizing", Winsorizer(limits=(0, 0.01))),
    ("lags", LagFeatureGenerator(n_lags=5))
])

