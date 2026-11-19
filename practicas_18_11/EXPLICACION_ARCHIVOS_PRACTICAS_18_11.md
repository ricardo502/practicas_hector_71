# Explicación de los archivos de `practicas_18_11`

Este documento explica la función de cada archivo de la carpeta, su lógica principal, los datos que utiliza y su relación con los demás programas.

La carpeta contiene un proyecto completo de **SmartAcademy**, que combina:

- MongoDB Atlas para almacenar información.
- Streamlit para crear interfaces web.
- Apache Spark para procesar muchos registros.
- Scikit-learn para modelos clásicos de Machine Learning.
- PyTorch para redes neuronales CNN 1D.

## Vista general del flujo

```text
p20generador_datos_masivos.py
              |
              v
p21carga_masiva_spark.py
              |
              v
p22persistencia_spark_atlas.py
              |
              v
MongoDB Atlas
              |
              +--> p16consultasinteligentes.py
              +--> p17dashboard_smartacademy.py
              +--> p17dashboard_smartacademyv2.py
              +--> p18evaluacion_smartacademy.py
              +--> p19registro_academico_integral.py

p23preparacion_datos_cnn.py --> p24entrenamiento_cnn1d.py --> p25comparacion_modelos.py

p26preparacion_prediccion_cnn.py --> p27entrenamiento_prediccion_cnn.py
```

---

## 1. `p16consultasinteligentes.py`

### Propósito

Realiza consultas y análisis estadísticos sobre los documentos almacenados en MongoDB Atlas.

### Qué hace

1. Lee las variables de conexión desde el archivo `.env`.
2. Construye la URI de MongoDB.
3. Se conecta a la base de datos.
4. Consulta todos los análisis registrados.
5. Busca estudiantes con riesgo estimado.
6. Agrupa estudiantes por perfil académico.
7. Calcula estadísticas generales.
8. Consulta los mejores resultados.
9. Exporta reportes en archivos CSV.

### Funciones importantes

- `validar_configuracion()`: verifica que existan las variables necesarias.
- `construir_uri()`: crea la dirección de conexión.
- `conectar_mongodb()`: abre la conexión con Atlas.
- `consultar_todos()`: recupera análisis generales.
- `consultar_riesgos()`: filtra registros con riesgo.
- `analizar_perfiles()`: agrupa por perfil académico.
- `generar_estadisticas()`: calcula indicadores generales.
- `consultar_mejores_resultados()`: busca las probabilidades más altas.
- `exportar_reportes()`: guarda los resultados en CSV.

### Dependencias

`pandas`, `pymongo`, `python-dotenv` y MongoDB Atlas.

### Idea principal

Este archivo funciona como una capa de análisis sobre los datos que ya existen en MongoDB.

---

## 2. `p17dashboard_smartacademy.py`

### Propósito

Construye un dashboard web con Streamlit para visualizar la información académica.

### Qué muestra

- Indicadores generales.
- Predicciones de aprobación.
- Perfiles obtenidos con K-Means.
- Características académicas.
- Visualizaciones PCA.
- Historial de evaluaciones.
- Filtros por diferentes características.
- Botón para descargar información en CSV.

### Flujo

1. Streamlit configura la página.
2. El programa se conecta a MongoDB.
3. Recupera documentos.
4. Convierte los documentos en un `DataFrame`.
5. Limpia y prepara los datos.
6. Construye gráficos e indicadores.
7. Permite al usuario filtrar la información.

### Dependencias

`streamlit`, `pandas`, `plotly`, `pymongo` y `python-dotenv`.

### Ejecución habitual

```powershell
streamlit run p17dashboard_smartacademy.py
```

---

## 3. `p17dashboard_smartacademyv2.py`

### Propósito

Es una segunda versión del dashboard académico.

### Diferencias principales respecto a la primera versión

Incluye más funciones de seguimiento:

- Estudiantes únicos.
- Evaluaciones acumuladas.
- Historial general.
- Seguimiento individual.
- Evolución de las evaluaciones.
- Información visible sobre la conexión.

### Estructura

Mantiene la misma base que el primer dashboard:

```text
conexión -> consulta -> preparación -> indicadores -> gráficas -> filtros
```

La versión `v2` debe considerarse una evolución más completa del dashboard original.

---

## 4. `p18evaluacion_smartacademy.py`

### Propósito

Permite capturar los datos de un estudiante y generar una evaluación individual.

### Proceso de evaluación

1. Captura información del estudiante.
2. Carga los modelos de Machine Learning existentes.
3. Predice si el estudiante aprobará.
4. Identifica su perfil académico usando K-Means.
5. Proyecta sus características utilizando PCA.
6. Obtiene recomendaciones académicas.
7. Guarda el resultado en MongoDB Atlas.
8. Permite consultar evaluaciones anteriores.

### Dependencia interna importante

```python
from unidad3_fia import p14motor_recomendaciones as motor
```

Ese módulo debe existir para que funcionen las recomendaciones.

### Dependencias

`streamlit`, `pandas`, `pymongo`, `certifi`, `python-dotenv` y los modelos previamente entrenados.

---

## 5. `p19registro_academico_integral.py`

### Propósito

Registra un expediente académico completo para un estudiante.

### Información que administra

- Datos generales del estudiante.
- Materias cursadas.
- Calificaciones parciales.
- Asistencias.
- Calificación final.
- Evaluaciones de inteligencia artificial.
- Historial académico.

### Colecciones de MongoDB utilizadas

- `estudiantes`
- `evaluaciones_academicas`
- `analisis_estudiantes`

### Funciones importantes

- `validar_calificacion()`: comprueba que la calificación sea válida.
- `calcular_calificacion_final()`: calcula el resultado final.
- `procesar_materias()`: transforma la información de las materias.
- `convertir_materias_documentos()`: prepara documentos para MongoDB.
- `guardar_estudiante()`: registra o actualiza el expediente.

### Idea principal

Es una aplicación de registro académico que también integra predicciones y análisis de IA.

---

## 6. `p20generador_datos_masivos.py`

### Propósito

Genera un conjunto grande de datos académicos sintéticos.

### Configuración principal

- 10,000 estudiantes.
- 5 materias por estudiante.
- 50,000 registros esperados.
- Semilla aleatoria `42`.

### Datos generados

Cada registro incluye información como:

- Identificador del estudiante.
- Materia.
- Calificaciones parciales.
- Asistencia.
- Tendencia académica.

### Salidas

Guarda los archivos en la carpeta:

```text
resultados_bigdata
```

Entre sus archivos de salida se encuentran:

- `smartacademy_50000.csv`
- `resumen_datos_masivos.csv`

### Idea principal

Este programa prepara la información que después será procesada por Spark.

---

## 7. `p21carga_masiva_spark.py`

### Propósito

Procesa el CSV masivo utilizando Apache Spark.

### Flujo

1. Crea una sesión Spark.
2. Lee el archivo CSV.
3. Valida las columnas y los valores.
4. Convierte tipos de datos.
5. Realiza transformaciones.
6. Calcula análisis estadísticos.
7. Guarda los datos en formato Parquet.

### Entrada

```text
resultados_bigdata/smartacademy_50000.csv
```

### Salidas

Guarda archivos Parquet y resúmenes procesados.

### Conceptos importantes

- `SparkSession`: punto de entrada para trabajar con Spark.
- `DataFrame`: tabla distribuida de Spark.
- Particiones: división del trabajo para procesar datos en paralelo.
- Parquet: formato columnar eficiente para análisis.

---

## 8. `p22persistencia_spark_atlas.py`

### Propósito

Guarda en MongoDB Atlas los datos procesados por Spark.

### Flujo

```text
Parquet -> Spark -> particiones -> operaciones bulk -> MongoDB Atlas
```

### Qué hace

1. Lee las variables de conexión.
2. Abre una sesión Spark.
3. Lee el archivo Parquet.
4. Divide los datos en particiones.
5. Abre una conexión independiente de MongoDB para cada partición.
6. Inserta documentos utilizando operaciones masivas.
7. Verifica cuántos documentos fueron almacenados.

### Consideración importante

El programa no comparte el mismo cliente MongoDB entre procesos de Spark. Cada partición crea su conexión, lo cual evita problemas con conexiones no serializables.

### Dependencias

`pyspark`, `pymongo`, `certifi` y `python-dotenv`.

---

## 9. `p23preparacion_datos_cnn.py`

### Propósito

Prepara los datos para entrenar una CNN 1D de clasificación.

### Variables de entrada

Canal de calificaciones:

```text
parcial1, parcial2, parcial3
```

Canal de asistencias:

```text
asistencia_p1, asistencia_p2, asistencia_p3
```

### Forma de los datos

Cada registro se transforma en:

```text
[2 canales, 3 posiciones temporales]
```

Para 50,000 registros:

```text
X = [50000, 2, 3]
y = [50000]
```

### Variable objetivo

La columna `tendencia` se convierte en números:

```text
Descendente = 0
Estable     = 1
Favorable   = 2
```

### Separación de datos

Divide los registros por estudiante:

- 70 % entrenamiento.
- 15 % validación.
- 15 % prueba.

Esto evita que un mismo estudiante aparezca en varios conjuntos.

### Salidas

Guarda archivos comprimidos `.npz` y metadatos `.json` para que los utilice `p24`.

---

## 10. `p24entrenamiento_cnn1d.py`

### Propósito

Entrena una red neuronal convolucional 1D para clasificar la tendencia académica.

### Entrada

Utiliza los archivos preparados por `p23`.

### Arquitectura

La red contiene:

1. Primera capa `Conv1d`.
2. `BatchNorm1d`.
3. Activación ReLU.
4. Segunda capa `Conv1d`.
5. Segunda normalización.
6. Pooling adaptativo.
7. Dropout.
8. Capa lineal final.

### Salida

Genera tres puntuaciones, una por clase:

```text
0 = Descendente
1 = Estable
2 = Favorable
```

### Entrenamiento

Utiliza:

- Función de pérdida para clasificación.
- Optimizador.
- Entrenamiento por épocas.
- Validación por época.
- Early stopping.
- Recuperación de los mejores pesos.

### Resultados

Calcula:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Matriz de confusión.

También guarda el modelo y las métricas para `p25`.

---

## 11. `p25comparacion_modelos.py`

### Propósito

Compara la CNN 1D contra un modelo Random Forest.

### Modelos comparados

1. CNN 1D con PyTorch.
2. Random Forest con Scikit-learn.

### Preparación para Random Forest

La CNN utiliza datos con forma:

```text
[registros, 2, 3]
```

Random Forest necesita una tabla de dos dimensiones, por lo que los datos se transforman a:

```text
[registros, 6]
```

Las seis características son:

- Calificación parcial 1.
- Calificación parcial 2.
- Calificación parcial 3.
- Asistencia parcial 1.
- Asistencia parcial 2.
- Asistencia parcial 3.

### Qué genera

- Tabla comparativa.
- Métricas en JSON.
- Gráfica comparativa.
- Modelo Random Forest guardado con `joblib`.

---

## 12. `p26preparacion_prediccion_cnn.py`

### Propósito

Prepara un problema diferente: predecir numéricamente la calificación del parcial 3.

### Variables de entrada

Para cada registro utiliza:

- Calificación del parcial 1.
- Calificación del parcial 2.
- Asistencia del parcial 1.
- Asistencia del parcial 2.

### Variable objetivo

```text
Calificación del parcial 3
```

### Forma de entrada

```text
X = [registros, 2 canales, 2 parciales]
y = [registros]
```

Los canales son:

```text
Canal 0: calificaciones parciales 1 y 2
Canal 1: asistencias parciales 1 y 2
```

### Validaciones

El programa comprueba:

- Identificadores válidos.
- Registros sin duplicados.
- Cinco materias por estudiante.
- Calificaciones entre 0 y 10.
- Asistencias entre 0 y 100.
- Ausencia de valores nulos e infinitos.

### Salidas

Guarda un archivo `.npz` y metadatos `.json` para `p27`.

---

## 13. `p27entrenamiento_prediccion_cnn.py`

### Propósito

Entrena una CNN 1D para regresión académica.

Su objetivo no es clasificar en categorías, sino predecir una calificación numérica.

### Entrada

Utiliza los datos preparados por `p26`.

### Proceso

1. Carga los arreglos `.npz`.
2. Crea los `Dataset` de PyTorch.
3. Construye los `DataLoader`.
4. Define la CNN de regresión.
5. Entrena el modelo.
6. Valida durante el entrenamiento.
7. Recupera los mejores pesos.
8. Predice el parcial 3 sobre el conjunto de prueba.

### Métricas

- `MAE`: error absoluto medio.
- `MSE`: error cuadrático medio.
- `RMSE`: raíz del error cuadrático medio.
- `R2`: proporción de variabilidad explicada.

### Modelo base

Compara la CNN contra una predicción sencilla basada en el promedio de las calificaciones. Esto permite saber si la red realmente aprende algo útil.

### Salidas

Guarda:

- Modelo entrenado.
- Historial de entrenamiento.
- Métricas.
- Gráfica de pérdida.
- Gráfica de valores reales contra predichos.
- Predicciones del conjunto de prueba.

---

## Archivo `Practicas_18_11_2026.rar`

Es un archivo comprimido relacionado con la carpeta. Puede contener una copia de las prácticas o archivos de respaldo. Los scripts principales que se analizaron son los archivos `.py` que están directamente en la carpeta.

---

## Orden recomendado para estudiar el proyecto

### Parte A: datos masivos

```text
p20 -> p21 -> p22
```

Primero se generan los datos, luego se procesan con Spark y finalmente se almacenan en MongoDB.

### Parte B: consultas y aplicaciones

```text
p16 -> p17 / p17v2 / p18 / p19
```

Después se consultan los datos, se muestran en dashboards y se construyen evaluaciones individuales o expedientes académicos.

### Parte C: clasificación con CNN

```text
p23 -> p24 -> p25
```

Se preparan los datos, se entrena una CNN para clasificar tendencias y se compara contra Random Forest.

### Parte D: regresión con CNN

```text
p26 -> p27
```

Se preparan entradas parciales y asistencias para predecir numéricamente la calificación del parcial 3.

## Diferencia entre clasificación y regresión

La clasificación de `p23` y `p24` responde a una pregunta como:

```text
¿La tendencia es descendente, estable o favorable?
```

La regresión de `p26` y `p27` responde a una pregunta como:

```text
¿Qué calificación numérica tendrá el parcial 3?
```

## Dependencias principales

```text
numpy
pandas
matplotlib
plotly
streamlit
pymongo
python-dotenv
certifi
pyspark
scikit-learn
torch
joblib
```

Además, algunas prácticas necesitan:

- Un archivo `.env` con las credenciales de MongoDB Atlas.
- Java para ejecutar Spark.
- El módulo interno `unidad3_fia`.
- Los archivos generados por las prácticas anteriores.

## Conclusión

La carpeta no contiene ejercicios aislados. Es una secuencia de etapas que construye un sistema académico completo:

1. Generación de datos.
2. Procesamiento masivo.
3. Persistencia en MongoDB.
4. Consultas y dashboards.
5. Evaluación individual.
6. Clasificación con CNN.
7. Comparación con Random Forest.
8. Predicción numérica mediante regresión.
