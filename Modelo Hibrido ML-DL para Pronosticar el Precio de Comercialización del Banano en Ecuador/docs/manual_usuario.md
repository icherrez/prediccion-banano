# Manual de Usuario – Modelo Hibrido ML-DL para Pronosticar el Precio de Comercialización del Banano en Ecuador

## 1. Descripción general

Esta aplicación permite **pronosticar el precio semanal de comercialización del banano en Ecuador** a partir de datos históricos.  
El modelo está basado en un **SuperLearner híbrido** que combina algoritmos de *Machine Learning* (Ridge, MLP, XGBoost) y *Deep Learning* (LSTM).

El sistema incluye una **interfaz gráfica amigable (Tkinter)** que facilita la carga de datos, la visualización del progreso del entrenamiento y la interpretación de los resultados.

---

## 2. Requisitos del sistema

### Hardware mínimo
- Procesador Intel/AMD (2 núcleos o más)
- 8 GB de memoria RAM
- 500 MB de espacio libre en disco
- GPU opcional (acelera el entrenamiento LSTM)

### Software
- **Sistema operativo:** Windows 10 o superior  
- **Python:** versión 3.10–3.12 (si se ejecuta el script)  
- **Librerías principales:**
  - `numpy`, `pandas`, `matplotlib`
  - `scikit-learn`
  - `xgboost`
  - `tensorflow`
  - `tkinter`

Si se utiliza el **ejecutable (.exe)**, no se requiere instalación previa de dependencias.

---

## 3. Inicio de la aplicación

Al ejecutar el programa (`Precio_Banano.exe` o `app.py`), se mostrará la ventana principal con las siguientes opciones:

- 🟢 **Usar datos demo:** carga el dataset `precio_ecuador.xlsx` incluido en `app/assets/`.
- 📂 **Cargar datos propios:** abre un diálogo para seleccionar un archivo `.xlsx` o `.xls` con tus datos históricos.

> **Formato esperado del archivo Excel:**
> - Columnas: `Año`, `Semana`, `Precio`
> - Al menos 10–15 observaciones consecutivas.
> - No deben existir semanas duplicadas o vacías.

Si el archivo no cumple el formato, se mostrará un mensaje de error y la ejecución se detendrá de forma segura.

---

## 4. Proceso de modelado

Una vez cargados los datos:

1. **Preprocesamiento automático:**
   - Generación de columna `Fecha` (basada en ISO Week).
   - Creación de 5 variables *lag* (`Precio_t-1` … `Precio_t-5`).
   - Escalado de características con `MinMaxScaler`.

2. **Entrenamiento de modelos base:**
   - Ridge Regression  
   - Multi-Layer Perceptron (MLP)  
   - XGBoost  
   - LSTM

3. **SuperLearner (meta-modelo):**
   - Combina las predicciones de los modelos base mediante un `RidgeCV`.
   - Se ajusta sobre validación cruzada temporal (`TimeSeriesSplit`).

4. **Pronóstico final:**
   - Se generan predicciones para las próximas **5 semanas**.
   - Los resultados se muestran en una tabla y gráfico continuo.

---

## 5. Interfaz gráfica

### Componentes principales
- **Ventana de progreso:** muestra el estado del entrenamiento y mensajes amigables ("Entrenamiento del modelo iniciado...").
- **Gráfico de resultados:** presenta las últimas 5 observaciones reales y las 5 semanas proyectadas.
- **Botón “Cerrar”:** permite finalizar la aplicación cuando el proceso concluye.

La ventana se ajusta automáticamente al contenido del texto y el gráfico.

---

## 6. Resultados mostrados

Al finalizar el proceso, se presentan:

| Semana | Ridge | MLP | XGB | LSTM | SuperLearner |
|:-------|------:|------:|------:|------:|------:|
| 43 | 1.095 | 1.091 | 1.088 | 1.090 | 1.089 |
| 44 | 1.097 | 1.094 | 1.091 | 1.093 | 1.092 |
| … | … | … | … | … | … |

El gráfico final muestra la continuidad entre los valores reales y los predichos para facilitar la interpretación visual de tendencias.

---


