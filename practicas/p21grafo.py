# ============================================================
# BÚSQUEDA CIEGA - DEPTH FIRST SEARCH (DFS)
# ============================================================
#
# DFS = Depth First Search
#      Búsqueda en Profundidad
#
# IDEA PRINCIPAL:
# DFS intenta avanzar lo más profundo posible por un camino
# antes de regresar y probar otro camino.
#
# Es una búsqueda CIEGA porque NO utiliza información adicional
# que indique qué tan cerca estamos del objetivo.
# ============================================================

# DFS conceptualmente utiliza una estructura tipo pila:

#          ┌─────┐
#entra →   │  A  │
#          │  B  │
#          │  D  │ ← sale primero
#          └─────┘
#            LIFO

# ------------------------------------------------------------
# 1. DEFINIMOS EL ESPACIO DE BÚSQUEDA
# ------------------------------------------------------------
#
# El diccionario representa un grafo.
#
# Cada clave representa un estado.
# La lista asociada contiene los estados vecinos
# a los que podemos desplazarnos.
#
# Visualmente podemos imaginar:
#
#              A
#             / \
#            B   C
#           / \   \
#          D   E   F
#             / \
#            G   H
#
# DFS comenzará en A y buscará llegar a H.
# ------------------------------------------------------------

import heapq

grafo = {
    "A": [("B", 2), ("C", 5)],
    
    "B": [("D", 4), ("E", 1)],
    
    "C": [("F", 2), ("G", 8)],
    
    "D": [("H", 3)],
    
    "E": [("I", 2)],
    
    "F": [("J", 3)],
    
    "G": [],
    
    "H": [],
    
    "I": [],
    
    "J": [],
}


def costo_uniforme(grafo, inicio, objetivo):
    """Devuelve la ruta de menor costo y su costo total."""
    pendientes = [(0, inicio, [inicio])]
    visitados = set()

    while pendientes:
        costo, actual, camino = heapq.heappop(pendientes)

        if actual in visitados:
            continue

        visitados.add(actual)
        print(f"Visitando: {actual} | Costo acumulado: {costo}")

        if actual == objetivo:
            return camino, costo

        for vecino, costo_conexion in grafo[actual]:
            if vecino not in visitados:
                heapq.heappush(
                    pendientes,
                    (costo + costo_conexion, vecino, camino + [vecino]),
                )

    return None, None


if __name__ == "__main__":
    inicio = "A"
    objetivo = "I"
    ruta, costo_total = costo_uniforme(grafo, inicio, objetivo)

    print(f"\nInicio: {inicio} | Objetivo: {objetivo}")
    if ruta:
        print("Ruta encontrada:", " -> ".join(ruta))
        print("Costo total:", costo_total)
    else:
        print("No se encontró una ruta.")
