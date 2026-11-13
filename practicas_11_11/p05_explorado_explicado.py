"""Práctica 05 explicada: comparación de algoritmos y experimentos.

Archivo independiente. No modifica p05algoritmosmachinelearning.py.

Se comparan tres modelos y después se cambia un parámetro de cada uno para
observar qué ocurre. Los resultados se guardan en CSV y PNG.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


CARPETA_RESULTADOS = Path(__file__).resolve().parent / "resultados_p05_explorado"
CARPETA_RESULTADOS.mkdir(exist_ok=True)
SEMILLA = 42


def crear_datos(cantidad=500):
    """Crea datos sintéticos con cuatro características y una clase objetivo."""
    rng = np.random.default_rng(SEMILLA)
    datos = pd.DataFrame({
        "horas_estudio": rng.uniform(0, 20, cantidad),
        "asistencia": rng.uniform(40, 100, cantidad),
        "actividades": rng.uniform(0, 100, cantidad),
        "participacion": rng.uniform(0, 10, cantidad),
    })

    # Normalizamos cada variable para combinarla en una escala parecida.
    puntaje = (
        datos["horas_estudio"] / 20 * 0.30
        + datos["asistencia"] / 100 * 0.25
        + datos["actividades"] / 100 * 0.30
        + datos["participacion"] / 10 * 0.15
        + rng.normal(0, 0.12, cantidad)
    )
    datos["aprueba"] = (puntaje >= 0.58).astype(int)
    return datos.drop(columns="aprueba"), datos["aprueba"]


def crear_modelos():
    """Devuelve modelos con configuraciones fáciles de comparar."""
    return {
        "Decision Tree": DecisionTreeClassifier(
            max_depth=5, min_samples_leaf=4, random_state=SEMILLA
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=200, min_samples_leaf=2,
            n_jobs=-1, random_state=SEMILLA
        ),
        # KNN necesita escalamiento; Pipeline lo hace dentro de cada ajuste.
        "KNN": Pipeline([
            ("escalador", StandardScaler()),
            ("clasificador", KNeighborsClassifier(
                n_neighbors=7, weights="distance"
            )),
        ]),
    }


def medir_modelo(modelo, X_entrenamiento, y_entrenamiento,
                 X_validacion, y_validacion):
    """Entrena un modelo y devuelve accuracy y F1 sobre validación."""
    modelo.fit(X_entrenamiento, y_entrenamiento)
    predicciones = modelo.predict(X_validacion)
    return {
        "accuracy": accuracy_score(y_validacion, predicciones),
        "f1": f1_score(y_validacion, predicciones, zero_division=0),
    }


def experimento(nombre, valores, construir_modelo,
                X_entrenamiento, y_entrenamiento,
                X_validacion, y_validacion):
    """Repite una prueba cambiando un solo parámetro."""
    filas = []
    for valor in valores:
        modelo = construir_modelo(valor)
        metricas = medir_modelo(
            modelo, X_entrenamiento, y_entrenamiento,
            X_validacion, y_validacion
        )
        filas.append({"experimento": nombre, "parametro": str(valor), **metricas})
    return pd.DataFrame(filas)


def main():
    print("PRACTICA 05 EXPLORADA Y EXPLICADA")
    X, y = crear_datos()

    # Separamos prueba antes de comparar. La prueba no participa en la elección.
    X_entrenamiento_validacion, X_prueba, y_entrenamiento_validacion, y_prueba = (
        train_test_split(X, y, test_size=0.20, random_state=SEMILLA, stratify=y)
    )
    X_entrenamiento, X_validacion, y_entrenamiento, y_validacion = (
        train_test_split(
            X_entrenamiento_validacion, y_entrenamiento_validacion,
            test_size=0.25, random_state=SEMILLA,
            stratify=y_entrenamiento_validacion,
        )
    )

    # Comparación inicial: tres algoritmos con una configuración base.
    filas = []
    modelos = crear_modelos()
    modelos_entrenados = {}
    for nombre, modelo in modelos.items():
        metricas = medir_modelo(
            modelo, X_entrenamiento, y_entrenamiento,
            X_validacion, y_validacion
        )
        modelos_entrenados[nombre] = modelo
        filas.append({"algoritmo": nombre, **metricas})
    comparacion = pd.DataFrame(filas).sort_values("f1", ascending=False)
    print("\nComparación inicial:")
    print(comparacion.to_string(index=False, formatters={
        "accuracy": "{:.2%}".format, "f1": "{:.2%}".format
    }))

    # Experimento A: el efecto de la cantidad de vecinos de KNN.
    knn = experimento(
        "KNN - n_neighbors", [3, 5, 7, 9, 15],
        lambda n: Pipeline([
            ("escalador", StandardScaler()),
            ("clasificador", KNeighborsClassifier(
                n_neighbors=n, weights="distance"
            )),
        ]),
        X_entrenamiento, y_entrenamiento, X_validacion, y_validacion,
    )

    # Experimento B: más árboles no garantiza automáticamente mejor resultado.
    bosque = experimento(
        "Random Forest - n_estimators", [50, 100, 200, 500],
        lambda n: RandomForestClassifier(
            n_estimators=n, min_samples_leaf=2,
            n_jobs=-1, random_state=SEMILLA
        ),
        X_entrenamiento, y_entrenamiento, X_validacion, y_validacion,
    )

    # Experimento C: profundidad y riesgo de subajuste/sobreajuste.
    arbol = experimento(
        "Decision Tree - max_depth", [2, 3, 5, 8, None],
        lambda profundidad: DecisionTreeClassifier(
            max_depth=profundidad, min_samples_leaf=4,
            random_state=SEMILLA
        ),
        X_entrenamiento, y_entrenamiento, X_validacion, y_validacion,
    )
    experimentos = pd.concat([knn, bosque, arbol], ignore_index=True)
    print("\nExperimentos:")
    print(experimentos.to_string(index=False, formatters={
        "accuracy": "{:.2%}".format, "f1": "{:.2%}".format
    }))

    # Elegimos el modelo base con mayor F1 de validación y lo reentrenamos con 80 %.
    mejor_nombre = comparacion.iloc[0]["algoritmo"]
    modelo_final = clone(crear_modelos()[mejor_nombre])
    modelo_final.fit(X_entrenamiento_validacion, y_entrenamiento_validacion)
    predicciones = modelo_final.predict(X_prueba)
    print("\nModelo elegido:", mejor_nombre)
    print("Accuracy final:", f"{accuracy_score(y_prueba, predicciones):.2%}")
    print("F1 final:", f"{f1_score(y_prueba, predicciones):.2%}")

    # Validación cruzada sobre entrenamiento + validación para observar estabilidad.
    cv = cross_val_score(
        clone(crear_modelos()[mejor_nombre]),
        X_entrenamiento_validacion, y_entrenamiento_validacion,
        cv=5, scoring="f1", n_jobs=-1,
    )
    print("F1 de validación cruzada:", cv)
    print("Promedio CV:", f"{cv.mean():.2%}")

    comparacion.to_csv(CARPETA_RESULTADOS / "comparacion_inicial.csv", index=False)
    experimentos.to_csv(CARPETA_RESULTADOS / "experimentos.csv", index=False)

    plt.figure(figsize=(11, 6))
    for nombre, grupo in experimentos.groupby("experimento"):
        plt.plot(grupo["parametro"], grupo["f1"], marker="o", label=nombre)
    plt.ylim(0, 1.05)
    plt.xlabel("Valor probado")
    plt.ylabel("F1-score de validación")
    plt.title("Efecto de cambiar parámetros")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(CARPETA_RESULTADOS / "experimentos_f1.png", dpi=200)
    plt.close()
    print(f"\nResultados guardados en: {CARPETA_RESULTADOS}")


if __name__ == "__main__":
    main()
