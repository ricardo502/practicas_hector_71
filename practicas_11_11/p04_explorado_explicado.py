"""Práctica 04 explicada: entrenamiento, validación y prueba.

Este archivo es una versión independiente y didáctica de la práctica original.
No modifica p04entrenamiento_validacion_prueba.py.

Idea principal:
    entrenamiento -> el modelo aprende
    validación    -> elegimos la configuración
    prueba        -> medimos el resultado final una sola vez
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier


# Guardamos los resultados junto a este archivo, sin depender del directorio
# desde el que se ejecute Python.
CARPETA_RESULTADOS = Path(__file__).resolve().parent / "resultados_p04_explorado"
CARPETA_RESULTADOS.mkdir(exist_ok=True)


def crear_datos(cantidad=500, semilla=42):
    """Genera datos ficticios y devuelve características X, objetivo y tabla."""
    rng = np.random.default_rng(semilla)

    datos = pd.DataFrame({
        "horas_estudio": rng.uniform(0, 15, cantidad),
        "asistencia": rng.uniform(30, 100, cantidad),
        "actividades": rng.uniform(10, 100, cantidad),
        "participacion": rng.uniform(0, 10, cantidad),
    })

    # Esta fórmula no representa estudiantes reales: solo crea un ejemplo.
    ruido = rng.normal(0, 7, cantidad)
    puntuacion = (
        datos["horas_estudio"] * 2.5
        + datos["asistencia"] * 0.25
        + datos["actividades"] * 0.15
        + datos["participacion"] * 1.5
        + ruido
    )
    datos["aprueba"] = (puntuacion >= 55).astype(int)

    X = datos.drop(columns="aprueba")
    y = datos["aprueba"]
    return X, y, datos


def evaluar_profundidades(X_entrenamiento, X_validacion,
                          y_entrenamiento, y_validacion):
    """Compara árboles pequeños y grandes usando validación."""
    profundidades = [1, 2, 3, 5, 10, None]
    resultados = []
    modelos = {}

    for profundidad in profundidades:
        modelo = DecisionTreeClassifier(
            max_depth=profundidad,
            random_state=42,
        )
        modelo.fit(X_entrenamiento, y_entrenamiento)

        pred_entrenamiento = modelo.predict(X_entrenamiento)
        pred_validacion = modelo.predict(X_validacion)

        resultados.append({
            "profundidad": "sin límite" if profundidad is None else profundidad,
            "entrenamiento": accuracy_score(
                y_entrenamiento, pred_entrenamiento
            ),
            "validacion": accuracy_score(y_validacion, pred_validacion),
        })
        modelos[profundidad] = modelo

    return pd.DataFrame(resultados), modelos


def main():
    print("PRACTICA 04 EXPLORADA Y EXPLICADA")

    # 1. Crear y observar los datos.
    X, y, datos = crear_datos()
    print("\nPrimeros registros:")
    print(datos.head())
    print("\nDistribución de clases:")
    print(y.value_counts().sort_index())

    # 2. Reservar datos que el modelo no verá durante el aprendizaje.
    X_entrenamiento, X_temporal, y_entrenamiento, y_temporal = train_test_split(
        X, y, test_size=0.40, random_state=42, stratify=y
    )
    X_validacion, X_prueba, y_validacion, y_prueba = train_test_split(
        X_temporal, y_temporal, test_size=0.50, random_state=42,
        stratify=y_temporal
    )
    print("\nTamaños: entrenamiento=", len(X_entrenamiento),
          "validación=", len(X_validacion), "prueba=", len(X_prueba))

    # 3. La validación sirve para elegir la profundidad, no la prueba.
    tabla, modelos = evaluar_profundidades(
        X_entrenamiento, X_validacion, y_entrenamiento, y_validacion
    )
    print("\nComparación de profundidades:")
    print(tabla.to_string(index=False, formatters={
        "entrenamiento": "{:.2%}".format,
        "validacion": "{:.2%}".format,
    }))

    indice_mejor = tabla["validacion"].idxmax()
    profundidad_texto = tabla.loc[indice_mejor, "profundidad"]
    profundidad = None if profundidad_texto == "sin límite" else int(profundidad_texto)
    mejor_modelo = modelos[profundidad]
    print("\nModelo elegido con validación:", profundidad_texto)

    # 4. Ahora sí usamos prueba, una sola vez, para estimar el desempeño final.
    predicciones = mejor_modelo.predict(X_prueba)
    metricas = {
        "accuracy": accuracy_score(y_prueba, predicciones),
        "precision": precision_score(y_prueba, predicciones, zero_division=0),
        "recall": recall_score(y_prueba, predicciones, zero_division=0),
        "f1": f1_score(y_prueba, predicciones, zero_division=0),
    }
    print("\nMétricas finales en prueba:")
    for nombre, valor in metricas.items():
        print(f"{nombre}: {valor:.2%}")
    print("\nMatriz de confusión:")
    print(confusion_matrix(y_prueba, predicciones, labels=[0, 1]))
    print(classification_report(
        y_prueba, predicciones,
        labels=[0, 1],
        target_names=["No aprueba", "Aprueba"],
        zero_division=0,
    ))

    # 5. Validación cruzada: varias divisiones para observar estabilidad.
    modelo_cv = DecisionTreeClassifier(max_depth=profundidad, random_state=42)
    puntuaciones = cross_val_score(
        modelo_cv, X_entrenamiento, y_entrenamiento,
        cv=5, scoring="accuracy"
    )
    print("Validación cruzada:", puntuaciones)
    print(f"Promedio CV: {puntuaciones.mean():.2%}")

    # 6. Gráfica y archivos para explorar los resultados.
    tabla.to_csv(CARPETA_RESULTADOS / "comparacion_profundidades.csv", index=False)
    pd.DataFrame([metricas]).to_csv(
        CARPETA_RESULTADOS / "metricas_finales.csv", index=False
    )

    plt.figure(figsize=(9, 5))
    x = range(len(tabla))
    plt.plot(x, tabla["entrenamiento"], marker="o", label="Entrenamiento")
    plt.plot(x, tabla["validacion"], marker="s", label="Validación")
    plt.xticks(list(x), tabla["profundidad"])
    plt.ylim(0, 1.05)
    plt.xlabel("Profundidad del árbol")
    plt.ylabel("Exactitud")
    plt.title("Entrenamiento frente a validación")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(CARPETA_RESULTADOS / "comparacion_profundidades.png", dpi=200)
    plt.close()

    print(f"\nResultados guardados en: {CARPETA_RESULTADOS}")


if __name__ == "__main__":
    main()
