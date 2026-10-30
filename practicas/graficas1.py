#"""
#==============================================================
#      Primer Gráfico con Matplotlib
#==============================================================

#Materia: Extracción de Conocimiento en Bases de Datos

#Objetivo: Aprender a construir una gráfica utilizando
#Matplotlib.

#==============================================================
#"""

# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================

import matplotlib.pyplot as plt
import numpy as np

# ==========================================================
# DATOS
# ==========================================================

# Horarios del día
horarios = [
    "Mañana\n06:00–11:59", "Tarde\n12:00–17:59",
    "Noche\n18:00–23:59", "Madrugada\n00:00–05:59"
]

# Datos simulados para demostrar el proyecto; no son estadísticas reales.
accidentes = [18, 30, 42, 24]

# ==========================================================
# CONFIGURACIÓN GENERAL ESTABLECE EL TAMAÑO DE LA FIGURA 
# ==========================================================

plt.figure(figsize=(14,8))

# ==========================================================
# GRÁFICA PRINCIPAL DIBUJA LA LINEA CON COLOR, GROSOR Y MARCADORES PERSONALIZADOS
# ==========================================================

plt.plot(
    horarios,
    accidentes,

    color="#1f77b4",

    linewidth=3,

    marker="o",

    markersize=8,

    markerfacecolor="white",

    markeredgewidth=2,

    label="Accidentes por horario"
)

# ==========================================================
# TÍTULO PRINCIPAL 
# ==========================================================

plt.title(
    "\n Accidentes vehiculares por horario",
    fontsize=22,
    fontweight="bold",
    pad=20
)


# ==========================================================
# SUBTÍTULO CON CONTEXTO
# ==========================================================

plt.suptitle(
    "Cámaras con sensores para prevenir accidentes | Datos simulados",
    fontsize=13,
    color="gray",
    y=0.93
)

# ==========================================================
# ETIQUETAS EN LOS EJES INDICANDO LA VARIABLE Y SUS UNIDADES
# ==========================================================

plt.xlabel(
    "Horario del día",
    fontsize=15,
    fontweight="bold"
)

plt.ylabel(
    "Cantidad de accidentes vehiculares",
    fontsize=15,
    fontweight="bold"
)

# ==========================================================
# CUADRÍCULA FACILITA LA LECTURA DE LOS VALORES 
# ==========================================================

plt.grid(
    linestyle="--",
    linewidth=0.7,
    alpha=0.6
)

# ==========================================================
# LEYENDA IDENTIFICA LOS ELEMENTOS REPRESENTADOS
# ==========================================================

plt.legend(
    fontsize=12,
    loc="upper left"
)

# ==========================================================
# ANOTACIONES MUESTRA EL VALOR EXACTO DE CADA OBSERVACIÓN 
# ==========================================================

for x, y in zip(horarios, accidentes):

    plt.text(
        x,
        y + 2,
        str(y),
        fontsize=10,
        ha="center"
    )

# ==========================================================
# LÍNEA DE PROMEDIO POR HORARIO
# ==========================================================

promedio = np.mean(accidentes)

plt.axhline(
    promedio,

    color="red",

    linestyle="--",

    linewidth=2,

    label="Promedio"
)

plt.text(
    3.4,
    promedio + 1,
    f"Promedio = {promedio:.1f}",
    color="red",
    fontsize=11,
    ha="right"
)

# ==========================================================
# DESTACAR EL HORARIO CON MÁS ACCIDENTES DEL EJEMPLO
# ==========================================================

indice_max = np.argmax(accidentes)

plt.scatter(
    horarios[indice_max],
    accidentes[indice_max],

    color="green",

    s=180,

    zorder=5,

    label="Máximo"
)

plt.annotate(
    "Más accidentesS ",

    xy=(horarios[indice_max], accidentes[indice_max]),

    xytext=(0.7, 48),

    arrowprops=dict(
        arrowstyle="->",
        color="green",
        lw=2
    ),

    fontsize=12
)

# ==========================================================
# PIE DE FIGURA INDICA LA FUENTE DE LOS DATOS Y EL AUTOR
# ==========================================================

plt.figtext(
    0.01,
    0.01,
    "Fuente: datos simulados del proyecto de cámaras con sensores | Elaboración propia | UTVT",
    fontsize=10,
    color="gray"
)

# ==========================================================
# QUITAR MARCO SUPERIOR Y DERECHO
# ==========================================================

ax = plt.gca()
ax.set_xlim(-0.2, 3.6)
ax.set_ylim(0, 55)

ax.spines["top"].set_visible(False)

ax.spines["right"].set_visible(False)

# ==========================================================
# AJUSTAR ESPACIOS
# ==========================================================

plt.tight_layout(rect=(0, 0.05, 1, 0.96))

# ==========================================================
# GUARDAR IMAGEN
# ==========================================================

plt.savefig(
    "Accidentes_Vehiculares_por_Horario.png",
    dpi=300,
    bbox_inches="tight"
)

# ==========================================================
# MOSTRAR
# ==========================================================

plt.show()

print("="*60)
print("Gráfica generada correctamente.")
print("Archivo guardado como:")
print("Accidentes_Vehiculares_por_Horario.png")
print("="*60)
