# prediccion-banano
# **UNIVERSIDAD DE ESPECIALIDADES ESPIRITU SANTO**

Proyecto Integrador en Inteligencia Artificial

PROFESORA: ING. GLADYS MARÍA VILLEGAS RUGEL

INTEGRANTES:

KEVIN OVALLE

IVAN CHÉRREZ

## **RESUMEN DEL PROBLEMA:**

**Objetivo general:** Desarrollar un modelo híbrido de machine learning para predecir semanalmente el precio de la caja de banano en Ecuador, midiendo su desempeño mediante RMSE, MAE y MAPE, con márgenes de errores al menos en 15% frente a modelos tradicionales en un plazo de seis semanas, contribuyendo a la mejora la capacidad de negociación del sector exportador.

**Objetivos específicos:**

1.Diseñar una base de datos estructurada a partir de series históricas de precios semanales de banano (2017–2025) para entrenar y evaluar los modelos.

2.Entrenar, ajustar y comparar al menos trece modelos de regresión (lineales, árboles de decisión, métodos de ensamble y redes neuronales) utilizando métricas de error estándar (RMSE, MAE, MAPE) en un conjunto de prueba independiente.

3.Implementar un modelo de Super Learner que integre los resultados de los modelos base para obtener un pronóstico más robusto y estable.

4.Validar la precisión del sistema mediante técnicas de validación cruzada y compararlo con benchmarks tradicionales (ETS, SARIMA).

5.Generar un informe técnico con los resultados y desarrollar un prototipo en Excel o Python que permita pronosticar las siguientes cinco semanas de precios como entregable funcional.


## **INFORMACIÓN DE DATASET:**

Dataset 1: Observatorio Estadístico de Banano (Precio Spot Semanal)
•Descripción técnica: Serie temporal semanal desde 2017 hasta 2025. Datos en formato Excel/CSV, con estructura organizada por semana y precio promedio ponderado.

•Procedencia: Observatorio Estadístico de Banano. Datos recolectados de un panel de 10 productores y 10 exportadores, con licencia restringida a suscriptores de la plataforma oficial https://observatoriobanano.com/precios.

•Calidad: Alta. Serie continua, representativa y construida con información validada directamente por actores clave del sector (gerentes de exportadoras y productores).

•Idoneidad: Muy alta. Constituye el insumo principal del proyecto al reflejar el precio spot de comercialización semanal en Ecuador, directamente relacionado con la toma de decisiones de negociación.

•Accesibilidad: Media. Aunque los datos están disponibles en formato digital y con actualizaciones semanales, el acceso requiere suscripción a la plataforma con un costo mensual de USD 180
