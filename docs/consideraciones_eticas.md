# Consideraciones Éticas del Proyecto

---

## 1. Análisis de sesgos

El dataset utilizado para entrenar el modelo de predicción del precio SPOT del banano no contiene sesgos demográficos ni personales, ya que trabaja con datos económicos y productivos agregados. Sin embargo, presenta **riesgos de sesgo estructural y geográfico**, dado que la información proviene de 10 productores y 10 exportadores de determinadas provincias, lo cual podría subrepresentar zonas rurales o cooperativas pequeñas con menor capacidad de reporte.

Estos sesgos podrían **afectar la equidad de las predicciones**, generando resultados más precisos para actores con mayor participación comercial y margen de maniobra financiera, mientras que los pequeños productores podrían recibir señales menos exactas.  
El grupo potencialmente más **perjudicado** serían los pequeños agricultores y cooperativas rurales con limitada representación digital o comercial, especialmente en provincias como Los Ríos, Guayas y El Oro, donde la heterogeneidad productiva es alta.

---

## 2. Equidad y Fairness

El modelo fue diseñado bajo principios de **equidad algorítmica**, buscando representar de forma balanceada a los distintos actores del sector bananero. Aunque no se utilizan métricas de fairness cuantitativas específicas (como demographic parity), se aplicaron criterios de representatividad muestral y validación cruzada geográfica para reducir sesgos.

**Estrategias implementadas:**
- Inclusión de observaciones de múltiples provincias y tamaños de finca.  
- Validación trimestral de representatividad mediante auditorías de datos.  
- Participación activa de productores y exportadores en la validación humana de resultados (human-in-the-loop).  
- Publicación de reportes de balance de datos con indicadores de diversidad y cobertura territorial.  

Estas acciones buscan asegurar que las predicciones sean **equitativas, reproducibles y verificables**, manteniendo justicia en la distribución de beneficios y riesgos.

---

## 3. Privacidad

El sistema no utiliza **datos personales ni sensibles**, ya que se basa exclusivamente en información estadística agregada: precios de venta, encuestas de mercado y variables económicas.  

**Mecanismos de protección implementados:**
- Anonimización de fuentes y exclusión de identificadores personales.  
- Almacenamiento en entornos seguros (repositorios con acceso restringido).  
- Publicación únicamente de datos agregados o promedios representativos.  

El proyecto cumple plenamente con la **Ley Orgánica de Protección de Datos Personales (LOPDP, Ecuador 2021)**, alineada con los principios del **RGPD europeo**, asegurando consentimiento informado, transparencia en el uso de datos y control sobre la información compartida.

---

## 4. Transparencia y Explicabilidad

El modelo mantiene un enfoque de **inteligencia artificial explicable (XAI)**. Aunque integra algoritmos complejos como XGBoost y LSTM, se han implementado mecanismos para facilitar su comprensión a los usuarios no técnicos.  

**Medidas adoptadas:**
- Documentación accesible en cada publicación del reporte semanal.  
- Glosario explicativo sobre las métricas (MAPE, RMSE) y el proceso de validación cruzada.  
- Incorporación de técnicas de interpretabilidad como **SHAP** (para modelos de árbol) y visualizaciones de sensibilidad para mostrar el impacto de cada variable en el resultado.  

De esta forma, los usuarios entienden que los precios proyectados son **estimaciones con margen de error**, no valores oficiales, preservando la confianza y comprensión del sistema.

---

## 5. Impacto Social

### Impactos Positivos
1. **Planificación económica mejorada:**  
   Los productores anticipan tendencias semanales, optimizando cosechas, logística y negociación.  
2. **Transparencia y democratización de la información:**  
   Nivelación del acceso a información de mercado entre actores grandes y pequeños.  
3. **Innovación tecnológica agrícola:**  
   Promueve la adopción de IA en cadenas productivas, fortaleciendo la competitividad nacional.

### Impactos Negativos
1. **Decisiones erróneas por predicciones inexactas:**  
   Pérdidas económicas en pequeños productores si las proyecciones son erróneas.  
2. **Brecha digital:**  
   Exclusión de agricultores con bajo acceso a internet o capacitación tecnológica.  
3. **Riesgo de manipulación:**  
   Posible uso oportunista de predicciones por actores con poder económico.

Los principales beneficiarios son los **productores medianos y exportadores** con acceso tecnológico, mientras que los grupos vulnerables son **pequeños agricultores** en regiones con baja conectividad.

---

## 6. Responsabilidad

La **rendición de cuentas (accountability)** está estructurada en una cadena clara de roles y responsabilidades:

| Rol | Responsabilidad | Rendición de cuentas |
|------|------------------|----------------------|
| **Desarrolladores** | Implementación técnica, validación del modelo, documentación. | Code reviews y reportes técnicos. |
| **Analistas del Observatorio** | Validación humana, comunicación de resultados, revisión semanal. | Bitácora de revisión y aprobación. |
| **Observatorio Estadístico de Banano** | Supervisión ética, gobernanza de datos y comunicación pública. | Comité técnico-ético semestral. |
| **Usuarios (Productores y Exportadores)** | Uso responsable y retroalimentación sobre pronósticos. | Reporte de discrepancias y capacitaciones. |

**Plan de monitoreo:**
- Validación semanal de resultados antes de publicación.  
- Auditoría técnica y ética cada seis meses.  
- Registro público de incidentes o errores en GitHub.  
- Comité técnico-ético permanente.  

En caso de error, se aplica un **protocolo de respuesta estructurado**: detección, retiro temporal del reporte, revisión del modelo, corrección, comunicación oficial y documentación del incidente.

---

## 7. Uso Dual y Mal Uso

El modelo fue diseñado para fines **educativos, gremiales y de apoyo a la toma de decisiones económicas**. Sin embargo, podrían existir riesgos de uso indebido, como manipular las proyecciones para influir en precios de mercado o decisiones de inversión.  

**Salvaguardas aplicadas:**
- Publicación controlada y simultánea de resultados a todos los usuarios.  
- Prohibición expresa de uso comercial o especulativo del modelo.  
- Inclusión de una cláusula de **“Términos de Uso Ético”** en cada versión del reporte.  
- Supervisión gremial por parte de la AEBE y el Observatorio.  

El modelo no puede ser empleado para **precios oficiales, predicciones financieras, ni decisiones automatizadas sin intervención humana.**

---

## 8. Limitaciones Reconocidas

**Casos donde NO debe usarse el modelo:**
- Como referencia oficial para contratos de exportación o precios mínimos garantizados.  
- Para decisiones de inversión sin validación técnica adicional.  
- En mercados distintos al bananero sin recalibración de variables y contextos.

**Advertencias a los usuarios:**
- Los resultados son **referenciales**, no determinantes.  
- Se deben contrastar con información climática, logística y del mercado internacional.  
- La precisión puede disminuir ante eventos exógenos como fenómenos climáticos o crisis logísticas.

**Casos límite:**
El modelo pierde confiabilidad en semanas con **cambios abruptos de precios internacionales**, anomalías meteorológicas extremas o falta temporal de datos. En tales casos, se recomienda suspender temporalmente las predicciones y comunicar la incertidumbre al público.

---

