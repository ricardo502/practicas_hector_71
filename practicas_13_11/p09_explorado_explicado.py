"""Práctica 09 explicada: reducción de dimensionalidad con PCA.

Versión independiente de p09pca.py. Genera datos si no existe el CSV de la
práctica anterior, para que pueda explorarse sin depender de otro archivo.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler


CARPETA = Path(__file__).resolve().parent / "resultados_p09_explorado"
CARPETA.mkdir(exist_ok=True)
VARIABLES = ["horas_estudio", "asistencia", "actividades", "participacion"]


def generar_datos():
    """Crea datos académicos ficticios para practicar PCA."""
    rng = np.random.default_rng(42)
    datos = pd.DataFrame({
        "horas_estudio": rng.uniform(0, 12, 500),
        "asistencia": rng.uniform(40, 100, 500),
        "actividades": rng.uniform(0, 30, 500),
        "participacion": rng.uniform(0, 100, 500),
    })
    return datos


def cargar_datos():
    """Usa el CSV de P7 si existe; de lo contrario crea datos de práctica."""
    ruta = Path(__file__).resolve().parent / "p07_estudiantes_segmentados.csv"
    if ruta.exists():
        datos = pd.read_csv(ruta)
        if all(columna in datos.columns for columna in VARIABLES):
            print("Se encontró el CSV de la práctica 7.")
            return datos
    print("No se encontró un CSV compatible; se generarán datos ficticios.")
    return generar_datos()


def preparar_datos(datos):
    """Selecciona variables numéricas y reemplaza valores faltantes."""
    X = datos[VARIABLES].apply(pd.to_numeric, errors="coerce")
    return X.fillna(X.median())


def main():
    print("PRACTICA 09 EXPLORADA Y EXPLICADA")
    datos = cargar_datos()
    X = preparar_datos(datos)

    # PCA depende de las escalas. Por ejemplo, asistencia está entre 0 y 100,
    # mientras que horas de estudio está entre 0 y 12.
    escalador = StandardScaler()
    X_estandarizado = escalador.fit_transform(X)

    # Primero conservamos las cuatro componentes para estudiar toda la varianza.
    pca_completo = PCA(n_components=len(VARIABLES))
    coordenadas = pca_completo.fit_transform(X_estandarizado)
    explicada = pca_completo.explained_variance_ratio_
    acumulada = np.cumsum(explicada)
    tabla_varianza = pd.DataFrame({
        "componente": ["PC1", "PC2", "PC3", "PC4"],
        "varianza_explicada": explicada,
        "varianza_acumulada": acumulada,
    })
    print("\nVarianza explicada:")
    print(tabla_varianza.to_string(index=False, formatters={
        "varianza_explicada": "{:.2%}".format,
        "varianza_acumulada": "{:.2%}".format,
    }))

    # Las cargas muestran cuánto aporta cada variable a cada componente.
    cargas = pd.DataFrame(
        pca_completo.components_, columns=VARIABLES,
        index=["PC1", "PC2", "PC3", "PC4"]
    )
    print("\nCargas de las componentes:")
    print(cargas.round(3))

    # Elegimos la cantidad mínima que alcanza al menos 85 % de varianza.
    cantidad = int(np.argmax(acumulada >= 0.85) + 1)
    pca_reducido = PCA(n_components=cantidad)
    coordenadas_reducidas = pca_reducido.fit_transform(X_estandarizado)
    reconstruccion_estandarizada = pca_reducido.inverse_transform(
        coordenadas_reducidas
    )
    error = mean_squared_error(X_estandarizado, reconstruccion_estandarizada)
    print(f"\nComponentes elegidas para conservar 85%: {cantidad}")
    print(f"Varianza acumulada conservada: {acumulada[cantidad - 1]:.2%}")
    print(f"Error medio de reconstrucción: {error:.6f}")

    # K-Means solo se usa para colorear la gráfica; PCA no recibe esas etiquetas.
    etiquetas = KMeans(n_clusters=3, n_init=20, random_state=42).fit_predict(
        X_estandarizado
    )
    reporte = datos.copy()
    reporte["cluster"] = etiquetas
    for indice in range(coordenadas.shape[1]):
        reporte[f"PC{indice + 1}"] = coordenadas[:, indice]

    tabla_varianza.to_csv(CARPETA / "varianza_pca.csv", index=False)
    cargas.to_csv(CARPETA / "cargas_pca.csv")
    reporte.to_csv(CARPETA / "coordenadas_pca.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, 5), explicada, marker="o", label="Individual")
    plt.plot(range(1, 5), acumulada, marker="s", label="Acumulada")
    plt.axhline(0.85, color="red", linestyle="--", label="Objetivo 85%")
    plt.xticks(range(1, 5), ["PC1", "PC2", "PC3", "PC4"])
    plt.ylim(0, 1.05)
    plt.ylabel("Proporción de varianza")
    plt.title("Varianza explicada por PCA")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(CARPETA / "varianza_pca.png", dpi=200)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.scatter(coordenadas[:, 0], coordenadas[:, 1], c=etiquetas,
                cmap="viridis", s=18)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("Estudiantes proyectados en dos componentes")
    plt.tight_layout()
    plt.savefig(CARPETA / "proyeccion_pca_2d.png", dpi=200)
    plt.close()
    print(f"Resultados guardados en: {CARPETA}")


if __name__ == "__main__":
    main()
