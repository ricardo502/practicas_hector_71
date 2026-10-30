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

grafo = {
    "A": [("B", 6), ("C", 4)],

    "B": [("D", 7), ("E", 5)],

    "C": [("F", 3), ("G", 6)],

    "D": [("H", 8)],

    "E": [],

    "F": [("I", 1)],

    "G": [],

    "H": [],

    "I": [("J", 0)],

    "J": []
}


# ------------------------------------------------------------
# 2. FUNCIÓN DE BÚSQUEDA
# ------------------------------------------------------------

def busqueda_voraz(actual, objetivo):

    # Cada pendiente guarda: estado, camino, costo de entrada
    # y costo total acumulado. A comienza con costo recorrido 0.
    pendientes = [(actual, [actual], 0, 0)]
    visitados = set()

    while pendientes:

        # ----------------------------------------------------
        # 3. ELEGIR EL ESTADO CON MENOR COSTO DE ENTRADA
        # ----------------------------------------------------
        pendientes.sort(key=lambda elemento: elemento[2])
        actual, camino, costo, costo_total = pendientes.pop(0)

        if actual in visitados:
            continue

        # ----------------------------------------------------
        # 4. MARCAR EL ESTADO ACTUAL COMO VISITADO
        # ----------------------------------------------------
        visitados.add(actual)
        print("Visitando:", actual, "| Costo de entrada:", costo)

        # ----------------------------------------------------
        # 5. COMPROBAR SI ENCONTRAMOS EL OBJETIVO
        # ----------------------------------------------------
        if actual == objetivo:
            return camino.copy(), costo_total

        # ----------------------------------------------------
        # 6. AGREGAR LOS VECINOS Y ACUMULAR EL COSTO
        # ----------------------------------------------------
        for vecino, costo_vecino in grafo[actual]:

            if vecino not in visitados:
                nuevo_camino = camino + [vecino]
                nuevo_costo = costo_total + costo_vecino
                pendientes.append(
                    (vecino, nuevo_camino, costo_vecino, nuevo_costo)
                )

    # --------------------------------------------------------
    # 7. TERMINAR SI NO EXISTE UNA RUTA
    # --------------------------------------------------------
    return None


# ============================================================
# 8. EJECUTAR LA BÚSQUEDA
# ============================================================

if __name__ == "__main__":
    resultado = busqueda_voraz("A", "J")

    # ========================================================
    # 9. MOSTRAR EL RESULTADO
    # ========================================================
    print("\nRuta encontrada:")

    if resultado:
        ruta, costo_total = resultado
        print(" -> ".join(ruta))
        print("Costo total:", costo_total)
    else:
        print("No se encontró una ruta.")
