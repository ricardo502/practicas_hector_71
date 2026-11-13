"""Práctica 08 explicada: explorar y evaluar grupos con K-Means.

Versión independiente de p08analisisavanzadoclusters.py.
Aquí se observa qué cambia al modificar la inicialización y el escalador.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler


CARPETA = Path(__file__).resolve().parent / "resultados_p08_explorado"
CARPETA.mkdir(exist_ok=True)
VARIABLES = ["horas_estudio", "asistencia", "actividades", "participacion"]


def generar_datos():
    """Genera tres perfiles ficticios sin entregar las etiquetas a K-Means."""
    rng = np.random.default_rng(42)
    alto = np.column_stack([
        rng.normal(8, 1, 180), rng.normal(92, 5, 180),
        rng.normal(27, 2, 180), rng.normal(90, 6, 180),
    ])
    medio = np.column_stack([
        rng.normal(5, 1, 170), rng.normal(75, 7, 170),
        rng.normal(20, 3, 170), rng.normal(65, 8, 170),
    ])
    bajo = np.column_stack([
        rng.normal(2.5, 1, 150), rng.normal(55, 8, 150),
        rng.normal(12, 4, 150), rng.normal(40, 10, 150),
    ])
    datos = np.vstack([alto, medio, bajo])
    rng.shuffle(datos)
    datos[:, 0] = np.clip(datos[:, 0], 0, 12)
    datos[:, 1] = np.clip(datos[:, 1], 0, 100)
    datos[:, 2] = np.clip(datos[:, 2], 0, 30)
    datos[:, 3] = np.clip(datos[:, 3], 0, 100)
    return pd.DataFrame(datos, columns=VARIABLES)


def ejecutar_kmeans(X, escalador, inicializacion="k-means++", semilla=42):
    """Escala los datos, entrena K-Means y devuelve etiquetas y calidad."""
    X_transformado = escalador.fit_transform(X)
    modelo = KMeans(
        n_clusters=3,
        init=inicializacion,
        n_init=20,
        random_state=semilla,
    )
    etiquetas = modelo.fit_predict(X_transformado)
    silueta = silhouette_score(X_transformado, etiquetas)
    return modelo, X_transformado, etiquetas, silueta


def main():
    print("PRACTICA 08 EXPLORADA Y EXPLICADA")
    datos = generar_datos()
    X = datos[VARIABLES]
    print("Estudiantes:", len(datos))
    print("Variables usadas:", VARIABLES)

    # Experimento A: K-Means++ elige centros iniciales de forma informada;
    # random los elige aleatoriamente. La silueta va de -1 a 1: más alta es mejor.
    filas_inicializacion = []
    resultados_modelos = {}
    for inicializacion in ["k-means++", "random"]:
        modelo, X_std, etiquetas, silueta = ejecutar_kmeans(
            X, StandardScaler(), inicializacion
        )
        filas_inicializacion.append({
            "inicializacion": inicializacion,
            "silhouette": silueta,
            "inercia": modelo.inertia_,
        })
        resultados_modelos[inicializacion] = (modelo, X_std, etiquetas)
    tabla_init = pd.DataFrame(filas_inicializacion)
    print("\nExperimento A - inicialización:")
    print(tabla_init.to_string(index=False))

    # Experimento B: cambiar la escala cambia las distancias, y K-Means usa distancias.
    filas_escalador = []
    for nombre, escalador in [
        ("StandardScaler", StandardScaler()),
        ("MinMaxScaler", MinMaxScaler()),
    ]:
        modelo, X_transformado, etiquetas, silueta = ejecutar_kmeans(
            X, escalador, "k-means++"
        )
        filas_escalador.append({
            "escalador": nombre,
            "silhouette": silueta,
            "inercia": modelo.inertia_,
        })
    tabla_escaladores = pd.DataFrame(filas_escalador)
    print("\nExperimento B - escaladores:")
    print(tabla_escaladores.to_string(index=False))

    # Experimento C: repetir el modelo con semillas distintas y comparar etiquetas.
    particiones = []
    for semilla in [1, 7, 21, 42, 99]:
        _, _, etiquetas, silueta = ejecutar_kmeans(
            X, StandardScaler(), "k-means++", semilla
        )
        particiones.append((semilla, etiquetas, silueta))
    referencia = particiones[0][1]
    tabla_estabilidad = pd.DataFrame([
        {
            "semilla": semilla,
            "silhouette": silueta,
            "ARI_vs_primera": adjusted_rand_score(referencia, etiquetas),
        }
        for semilla, etiquetas, silueta in particiones
    ])
    print("\nExperimento C - estabilidad:")
    print(tabla_estabilidad.to_string(index=False))

    # Modelo final: StandardScaler y K-Means++.
    modelo, X_std, etiquetas, silueta = ejecutar_kmeans(
        X, StandardScaler(), "k-means++"
    )
    datos_reporte = datos.copy()
    datos_reporte["cluster"] = etiquetas
    centroides = pd.DataFrame(
        modelo.cluster_centers_, columns=VARIABLES
    )
    # Distancia al centroide: valores altos son candidatos a revisar, no diagnósticos.
    distancias = np.linalg.norm(X_std - modelo.cluster_centers_[etiquetas], axis=1)
    datos_reporte["distancia_centroide"] = distancias
    umbral = np.percentile(distancias, 95)
    candidatos = datos_reporte[distancias >= umbral].copy()
    print(f"\nSilueta final: {silueta:.3f}")
    print("Posibles atípicos:", len(candidatos))

    tabla_init.to_csv(CARPETA / "comparacion_inicializaciones.csv", index=False)
    tabla_escaladores.to_csv(CARPETA / "comparacion_escaladores.csv", index=False)
    tabla_estabilidad.to_csv(CARPETA / "estabilidad_ari.csv", index=False)
    centroides.to_csv(CARPETA / "centroides.csv", index=False)
    datos_reporte.to_csv(CARPETA / "segmentos.csv", index=False)
    candidatos.to_csv(CARPETA / "posibles_atipicos.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.scatter(X_std[:, 0], X_std[:, 1], c=etiquetas, cmap="viridis", s=18)
    plt.xlabel("Horas de estudio estandarizadas")
    plt.ylabel("Asistencia estandarizada")
    plt.title("Segmentos encontrados por K-Means")
    plt.tight_layout()
    plt.savefig(CARPETA / "segmentos_2d.png", dpi=200)
    plt.close()
    print(f"Resultados guardados en: {CARPETA}")


if __name__ == "__main__":
    main()
