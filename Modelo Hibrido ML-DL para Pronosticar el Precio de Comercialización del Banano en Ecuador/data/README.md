# Dataset – Observatorio Estadístico de Banano

Este directorio contiene los datos utilizados para el desarrollo y validación del modelo predictivo de precios del banano en Ecuador.

## Descripción general

El conjunto de datos fue proporcionado por el **Observatorio Estadístico de Banano**, entidad que recopila información semanal desde 2017 hasta 2025 a partir de un panel compuesto por 10 productores y 10 exportadores del sector bananero ecuatoriano.

Los datos se obtienen bajo una licencia restringida para suscriptores a través de la plataforma oficial:  
🔗 [https://observatoriobanano.com/precios](https://observatoriobanano.com/precios)

Este dataset constituye la base principal para el entrenamiento, validación y evaluación del modelo predictivo desarrollado en este proyecto.

---

## Estructura del dataset

| Variable | Tipo de dato | Descripción |
|-----------|---------------|--------------|
| **Año** | `int64` | Año calendario correspondiente a la observación. |
| **Semana** | `int64` | Semana del año (1–52) en que se registró el precio. |
| **Precio** | `float64` | Precio promedio semanal del banano (USD por caja). |

**Dimensiones:**  
- Total de registros: **453**  
- Total de columnas: **3**  
- Tamaño en memoria: **≈ 10.7 KB**

---

## 🕒 Rango temporal y frecuencia

- **Rango de años:** 2017 – 2025  
- **Frecuencia:** Semanal  
- **Total de observaciones:** 453 semanas consecutivas  
- **Estado:** Serie completa y sin valores faltantes  

---

## 🧾 Ejemplo de datos

| Año | Semana | Precio |
|-----|---------|--------|
| 2017 | 1 | 3.30 |
| 2017 | 2 | 3.40 |
| 2017 | 3 | 5.60 |
| 2017 | 4 | 7.60 |
| 2017 | 5 | 7.20 |
| ... | ... | ... |
| 2025 | 34 | 6.85 |

---

## Uso previsto

Este dataset está diseñado para su uso en:
- Modelos de predicción de precios mediante aprendizaje automático y series temporales.  
- Análisis de tendencias y estacionalidades del mercado bananero.  
- Identificación de anomalías y patrones de comportamiento a lo largo del tiempo.

---

## Licencia y restricciones

> **Nota importante:**  
> Los datos contenidos en esta carpeta son ficticios y generados con fines exclusivamente demostrativos y académicos.  
> Aunque se basan en la estructura, variables y rangos observados en el conjunto de datos real, no representan información real ni confidencial del sector.
>
> Por razones de confidencialidad y cumplimiento de licencias, **no se publican los datos reales**, sino una **versión sintética** que mantiene la coherencia temporal y estadística necesaria para replicar el flujo de trabajo del proyecto.


---

**Última actualización:** Octubre 2025

