# Planificación del Proyecto: Modelo Híbrido ML-DL para Pronosticar el Precio de Comercialización del Banano en Ecuador

## 1. Definición del problema y objetivos

### Problema
El precio de comercialización de la caja de banano en Ecuador se publica con un rezago de una semana, lo que limita la capacidad de productores y exportadores para negociar con compradores locales. Este desfase genera incertidumbre en un mercado volátil, afectado por factores externos como el clima, los costos logísticos y la demanda global. Disponer de un modelo que pronostique el precio semanal en tiempo real permitiría mejorar la planificación logística y fortalecer las negociaciones comerciales. El reto consiste en desarrollar un sistema comparable con los modelos tradicionales, pero capaz de capturar variaciones provocadas por *shocks* externos.

### Objetivo general
Desarrollar un modelo híbrido de machine learning y deep learning para predecir semanalmente el precio de la caja de banano en Ecuador, midiendo su desempeño mediante RMSE, MAE y MAPE, con márgenes de error inferiores al 15% frente a modelos tradicionales, en un plazo de seis semanas.

### Objetivos específicos
1. Diseñar una base de datos estructurada con series históricas semanales (2017–2025).  
2. Entrenar y comparar al menos tres modelos de machine learning y deep learning .  
3. Implementar un modelo de *Super Learner* que integre los resultados de los modelos base.  
4. Validar la precisión del sistema mediante validación cruzada.  
5. Generar un informe técnico y un prototipo funcional que pronostique cinco semanas futuras.

---

## 2. Justificación de la relevancia del proyecto

La literatura muestra un vacío en la aplicación de metodologías híbridas y de ensamble en series de precios agrícolas con frecuencia semanal. La mayoría de estudios se centra en commodities con periodicidad mensual o diaria (arroz, trigo, maíz), sin considerar productos tropicales de exportación como el banano.  
Este proyecto aborda tres limitaciones clave:  
(i) escasa integración de variables exógenas,  
(ii) falta de modelos adaptados a choques externos en mercados emergentes, y  
(iii) débil aplicabilidad práctica para la toma de decisiones en tiempo casi real.  

El desarrollo del modelo *Super Learner* permitirá mejorar la precisión predictiva respecto a modelos convencionales y ofrecer un marco replicable a otros productos agrícolas estratégicos.

---

## 3. Alcance

### Alcance incluido
- Desarrollo de un modelo de predicción semanal basado en aprendizaje supervisado y métodos de ensamble.  
- Procesamiento de datos históricos de precios semanales (2017–2025).  
- Entrenamiento de trece modelos base y un meta-modelo *Super Learner*.  
- Evaluación mediante RMSE, MAE y MAPE, con validación cruzada.  
- Elaboración de reportes técnicos y visualizaciones comparativas.  
- Entrega de un prototipo funcional en Excel o Python para uso por productores y exportadores.

### Alcance excluido
- Predicción de volúmenes de producción o exportaciones.  
- Inclusión de variables exógenas (clima, logística, competencia internacional).  
- Desarrollo de aplicaciones web o móviles.  
- Escalamiento a entornos *big data* o de alta disponibilidad.

### Criterios de aceptación
- MAPE ≤ 15% (aceptable) y meta óptima cercana al 10%.  
- Entregables: base de datos estructurada, resultados comparativos, modelo *Super Learner* implementado, prototipo funcional y reporte técnico final.  
- Validación mediante comparación con ETS y SARIMA.  
- Calidad medida por reproducibilidad del código y precisión de métricas.

---

## 4. Cronograma de desarrollo

| Semana | Hito | Entregable principal (Planificado) | Estado planificado | Actividad Realizada | Estado real |
|:------:|:------|:----------------------------------|:------------------|:--------------------|:------------|
| 1 | Base de datos consolidada y limpia | Dataset 2017–2025 en formato reproducible (Excel/CSV) | ✅ | Se consolidó el dataset histórico con revisión de valores atípicos y creación de nuevas variables temporales para los rezagos. | ✅ |
| 1–2 | Arquitectura técnica definida | Repositorio estructurado con pipelines de datos y dependencias documentadas | ✅ | Se implementó una estructura modular en Python y GitHub, integrando notebooks de entrenamiento y validación. | ✅ |
| 2 | Análisis exploratorio (EDA) | Reporte con gráficos de serie temporal, distribución y estacionalidad | ✅ | Se realizó un EDA ampliado con análisis de correlaciones y autocorrelaciones entre semanas, visualizaciones de tendencia y variabilidad semanal. | ✅ |
| 3 | Modelos base y benchmarks tradicionales | Entrenamiento de regresión lineal, árboles de decisión, ETS y SARIMA | ✅ | Se ajustaron modelos Ridge, MLP, XGBoost y LSTM. | ✅ |
| 4 | Modelos de ensamble y red neuronal simple | Entrenamiento de Random Forest, XGBoost y MLPRegressor | ✅ | Se abordaron las **consideraciones éticas del proyecto**, asegurando trazabilidad y transparencia del modelo; además se inició el desarrollo de la aplicación ejecutable. | ✅ |
| 5 | Optimización y validación avanzada | Ajuste de hiperparámetros y validación cruzada de modelos base | ✅ | Se realizó la **optimización del Super Learner**, ajustando hiperparámetros de Ridge, MLP, XGBoost y LSTM y validando con k-fold cross-validation. | ✅ |
| 6 | Implementación del Super Learner y presentación final | Integración de modelos, reporte técnico y prototipo con predicciones de 5 semanas | ✅ | Se finalizó el Super Learner, integrando todos los modelos en una aplicación funcional ejecutable; se elaboró la documentación técnica y presentación final. | ✅ |


---

## 5. Recursos necesarios

### Recursos humanos
Equipo de dos desarrolladores/analistas de datos con roles compartidos en modelado, validación y documentación.  
Dedicación estimada total: **232 horas** distribuidas en 4 *sprints* de 6 semanas.  

### Recursos técnicos
- **Software:** Python (Google Colab), Excel, GitHub, PowerPoint.  
- **Librerías:** *scikit-learn*, *statsmodels*, *xgboost*, *pandas*, *matplotlib*.  
- **Infraestructura:** Computadoras personales y entorno gratuito de GPU en Google Colab.  

### Recursos financieros
Basados en horas-hombre equivalentes.  
- 85% horas de dedicación técnica.  
- 15% contingencias (consultoría o datasets externos).  

### Gestión de recursos
Los recursos están disponibles desde el inicio y se administran bajo metodología *Scrum*, con revisiones al final de cada sprint.

---

## 6. Riesgos identificados y mitigación

| Riesgo | Descripción | Estrategia de mitigación |
|:-------|:-------------|:-------------------------|
| Retrasos en limpieza de datos | Datos faltantes o inconsistentes | Uso de scripts modulares de imputación automática |
| Problemas de configuración técnica | Incompatibilidades de dependencias | Adopción de *frameworks* estándar (scikit-learn, statsmodels) |
| Entrenamiento lento | Limitaciones de hardware en Colab | Entrenar con subconjuntos reducidos y escalar gradualmente |
| *Overfitting* | Modelos con alta complejidad | Regularización y validación cruzada k-fold |
| Métricas no alcanzan nivel deseado | RMSE/MAPE altos en validación | Ajuste de hiperparámetros y nuevas particiones |
| Falta de tiempo en documentación | Sobrecarga al cierre del proyecto | Dedicación exclusiva en la última semana |
| Integración compleja del *Super Learner* | Fallos de compatibilidad entre modelos | Implementación modular incremental y pruebas por etapas |

