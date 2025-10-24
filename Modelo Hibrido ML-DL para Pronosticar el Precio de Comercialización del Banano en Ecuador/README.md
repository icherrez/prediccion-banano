# Modelo Híbrido ML-DL para Pronosticar el Precio de Comercialización del Banano en Ecuador

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![Model](https://img.shields.io/badge/Model-SuperLearner-orange.svg)

> Sistema predictivo basado en inteligencia artificial para estimar el precio de comercialización semanal del banano ecuatoriano. Combina algoritmos de machine learning clásicos y de deep learning bajo un enfoque SuperLearner optimizado, brindando soporte a la planificación económica y comercial del sector agrícola.

---

## Tabla de Contenidos
1. [Descripción del problema](#-descripción-del-problema)
2. [Dataset](#-dataset)
3. [Metodología](#-metodología)
4. [Resultados](#-resultados)
5. [Instalación y uso](#-instalación-y-uso)
6. [Interfaz de usuario](#-interfaz-de-usuario)
7. [Estructura del proyecto](#-estructura-del-proyecto)
8. [Consideraciones éticas](#-consideraciones-éticas)
9. [Autores y contribuciones](#-autores-y-contribuciones)
10. [Licencia](#-licencia)
11. [Agradecimientos y referencias](#-agradecimientos-y-referencias)

---

## Descripción del problema

El proyecto busca resolver la **falta de herramientas predictivas confiables y actualizadas** para estimar el precio de comercialización semanal del banano, uno de los principales productos de exportación del Ecuador.  
En la actualidad, productores y exportadores dependen de información retrospectiva o de estimaciones manuales, lo que dificulta la planificación de cosechas, la negociación contractual y la gestión de riesgos ante la volatilidad del mercado.

El sistema propuesto permite generar **pronósticos semanales del precio de la caja de banano** con un margen de error inferior al 15%, favoreciendo decisiones informadas en los distintos niveles de la cadena de valor.  

**Usuarios objetivo:** productores, exportadores, gremios agrícolas y analistas económicos.

---

## Dataset

**Descripción:**  
Base de datos semanal que integra precios SPOT, variables climáticas y encuestas a productores y exportadores realizadas por el Observatorio Estadístico de Banano (OEB).  

**Características principales:**
- Periodo: 2017–2025  
- Frecuencia: semanal  
- Variables: `Precio`, `Semana`, `Temperatura`, `Precipitación`, `Exportaciones`, `Enfunde`  
- Observaciones: 400 aprox.  
- Tipo de datos: numéricos y series temporales  

**Fuente:** Observatorio Estadístico de Banano – AEBE  
**Licencia:** Uso académico y gremial, bajo acuerdo de confidencialidad  
**Link (versión pública):** [Repositorio de datos anonimizados](https://github.com/icherrez/prediccion-banano/edit/main/Modelo%20Hibrido%20ML-DL%20para%20Pronosticar%20el%20Precio%20de%20Comercializaci%C3%B3n%20del%20Banano%20en%20Ecuador/data)

---

## Metodología

**Tipo de modelo:**  
Modelo híbrido tipo **SuperLearner**, compuesto por los algoritmos Ridge, MLP, XGBoost y LSTM, integrados mediante un meta-modelo RidgeCV.  

**Preprocesamiento aplicado:**
- Limpieza y creación de rezagos (`lags`)
- Escalado Min–Max
- División temporal (entrenamiento, validación y test)
- Manejo de outliers y datos faltantes

**Optimización:**  
Se aplicó una búsqueda sistemática y análisis de sensibilidad para ajustar hiperparámetros clave, garantizando estabilidad y precisión.  
Los experimentos se realizaron bajo **validación cruzada temporal (TimeSeriesSplit)**.

**Métricas de evaluación:**
- RMSE (Raíz del Error Cuadrático Medio)
- MAE (Error Absoluto Medio)
- MAPE (Error Porcentual Absoluto Medio)

---

## Resultados

**Comparativa de modelos base y ensamble optimizado**

| Modelo | RMSE | MAE | MAPE (%) |
|:--------|------:|------:|------:|
| Ridge | 1.260 | 1.021 | 11.42 |
| MLP | 1.219 | 1.027 | 11.79 |
| LSTM | 1.434 | 1.185 | 13.58 |
| XGB | 1.440 | 1.180 | 13.72 |
| **SuperLearner Mejorado (TEST)** | **1.320** | **1.071** | **11.84** |

**Conclusión:**  
La optimización redujo el MAPE en un 11.2%, consolidando un modelo robusto y replicable para la predicción de precios agrícolas.

---

## Instalación y uso

### Requisitos
- Python 3.10+  
- Librerías: `numpy`, `pandas`, `matplotlib`, `scikit-learn`, `xgboost`, `tensorflow`, `seaborn`

### Instalación

## Estructura del proyecto

---
## Consideraciones éticas

El modelo cumple con la **Ley Orgánica de Protección de Datos Personales (LOPDP, Ecuador 2021)** y los principios de inteligencia artificial responsable: **equidad, transparencia, privacidad y accountability**.  
No utiliza información personal y aplica **revisión humana (human-in-the-loop)** antes de la publicación de cada pronóstico.

### Limitaciones conocidas
- Sesgo potencial por subrepresentación de productores pequeños.  
- Dependencia excesiva de usuarios sin validación empírica.  
- Menor precisión en escenarios de volatilidad internacional extrema.  

### Advertencia
El modelo no debe usarse como fuente oficial de precios ni para decisiones financieras automatizadas.  
Ver detalle completo en [docs/consideraciones_eticas.md](./docs/consideraciones_eticas.md)

---

## Autores y contribuciones

| Nombre | Rol |
|:--------------------|:--------------------------------------------|
| **Kevin Ovalle** | Data Manager, diseño, modelado y validación |
| **Iván Cherrez** | Investigador, documentación técnica y ética |
| **Equipo OEB – AEBE** | Apoyo en provisión y verificación de datos |

---

## Licencia

Este proyecto se distribuye bajo la licencia **MIT**, permitiendo su uso y modificación con fines académicos y de investigación, siempre citando la fuente y sin alterar su propósito original.

---

## Agradecimientos y referencias

El equipo expresa su profundo agradecimiento a la **Asociación de Exportadores de Banano del Ecuador (AEBE)**, en especial al **director del Observatorio Estadístico de Banano (OEB), Paúl Vera**, por permitir el uso de los datos del OEB.  
Sin esta valiosa información, este proyecto no habría sido posible.

---

## Referencias

[1] Khiem, N. M., et al. (2022). *A novel machine learning approach to predict the export price of seafood products...* PLOS ONE, 17(9), e0275290.  
[2] Al-Azab, F., & Jaradat, S. A. (2019). *Comparison of ANN and ARIMA models for cereal price forecasting.* Journal of Economics and Sustainable Development, 10(2).  
[3] Zhang, Q., Wang, Y., & Li, Y. (2019). *Agricultural futures price forecasting using LSTM and SVR models.* Computers and Electronics in Agriculture, 167.  
[4] Dave, D., & Singh, R. (2021). *Machine learning models for retail price forecasting in India.* International Journal of Forecasting and Data Science, 6(3).  
[5] Hamad, H., Al-Dulaimi, M., & Al-Taie, F. (2023). *Forecasting agricultural commodity prices using ARIMA, SARIMA and Prophet.* Agricultural Economics Review, 24(1).  
[6] Suler, J., Henseler, M., & Jongeneel, T. (2021). *Forecasting EU maize prices with econometric and deep learning models.* European Review of Agricultural Economics, 48(5).  
[7] Ranjit, R., & Sharma, A. (2022). *Application of machine learning in rice price prediction in India.* International Journal of Agricultural Technology, 18(4).  
[8] Theofilou, D. (2025). *Hybrid ML approaches for dairy product price forecasting in the EU.* Journal of Agricultural Economics and Policy, 57(2).  
[9] Mulla, R. (2020). *Comparison of ARIMA and ANN models for vegetable price prediction in India.* International Journal of Data Science and Forecasting, 2(1).  
[10] Kumari, P., & Singh, R. (2023). *Forecasting wheat prices in India using ARIMA, SVR, and LSTM models.* Journal of Agricultural Informatics, 14(1).  
[11] Chi, C., Zhang, L., & Sun, X. (2022). *Deep learning models for rice price forecasting in China.* Information Processing in Agriculture, 9(3).  
[12] Si, H., Zhang, W., Wu, J., Lin, K., & Chen, J. (2022). *A review of price forecasting technology of fresh agricultural products.* ICBDC Proceedings.  
[13] Tran, Q., Pham, T., & Nguyen, H. (2023). *Hybrid ARIMA–LSTM model for forecasting agricultural prices in Vietnam.* Journal of Agricultural Informatics, 14(2).  
[14] Manogna, R. L., & Mishra, A. K. (2021). *Modeling and forecasting agricultural commodity prices.* Journal of Agricultural Economics, 72(4).  
[15] Manogna, R. L., & Mishra, A. K. (2025). *Machine learning models for forecasting agricultural commodity prices.* Agricultural Economics, 56(1).  
[16] Hachmi, H., El Idrissi, M., & Ait Lahcen, A. (2023). *Forecasting cereal prices in Morocco using deep learning.* African Journal of Agricultural and Resource Economics, 18(3).  
[17] Oktoviany, P., Knobloch, R., & Korn, R. (2021). *A ML-based price state prediction model for agricultural commodities.* Decisions in Economics and Finance, 44.  
[18] Avinasha, G., et al. (2023). *Hidden Markov guided deep learning models for forecasting highly volatile agricultural commodity prices.* Applied Soft Computing.  
[19] Chen, Z., et al. (2021). *Automated agriculture commodity price prediction system with ML techniques.* ASTES Journal, 6(2).  
[20] Kang, K., Lee, J., & Park, H. (2024). *Hybrid ARIMA–LSTM model for vegetable price forecasting in South Korea.* Journal of Computational and Applied Mathematics, 427.

