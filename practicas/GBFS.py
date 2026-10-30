import heapq

# ============================================================
# GBFS - GREEDY BEST FIRST SEARCH
# BÚSQUEDA VORAZ PRIMERO EL MEJOR
# ==========================================================


grafo = {
    "A": [("B", 20), ("C", 15)],

    "B": [("D", 18), ("E", 30)],

    "C": [("F", 10), ("G", 25)],

    "D": [("H", 40)],

    "E": [],

    "F": [("I", 5)],

    "G": [],

    "H": [],

    "I": [("J", 0)],

    "J": []
}

estado_inicial = "A"
estado_objetivo = "J"
estimacion_inicial = 25


# ------------------------------------------------------------
# 2. FUNCIÓN GBFS CON COLA DE PRIORIDAD
# ------------------------------------------------------------
def gbfs(inicial, objetivo):

    # Cada entrada contiene (heurística, estado, camino, valores del camino).
    # Los valores se guardan para mostrar su suma, sin afectar la prioridad.
    cola_prioridad = []
    heapq.heappush(
        cola_prioridad,
        (estimacion_inicial, inicial, [inicial], [estimacion_inicial])
    )
    visitados = set()

    while cola_prioridad:

        # ----------------------------------------------------
        # 3. EXTRAER EL ESTADO CON MENOR HEURÍSTICA
        # ----------------------------------------------------
        # heappop devuelve la entrada de menor valor h(n).
        heuristica, actual, camino, valores = heapq.heappop(cola_prioridad)

        if actual in visitados:
            continue

        # ----------------------------------------------------
        # 4. MARCAR Y MOSTRAR EL ESTADO VISITADO
        # ----------------------------------------------------
        visitados.add(actual)
        print(f"Visitando: {actual} | h({actual}) = {heuristica}")
        print("Recorrido:", " -> ".join(camino))

        # ----------------------------------------------------
        # 5. COMPROBAR SI LLEGAMOS AL OBJETIVO
        # ----------------------------------------------------
        if actual == objetivo:
            return camino, valores

        # ----------------------------------------------------
        # 6. INSERTAR LOS VECINOS EN LA COLA DE PRIORIDAD
        # ----------------------------------------------------
        for vecino, estimacion in grafo[actual]:
            if vecino not in visitados:
                nuevo_camino = camino + [vecino]
                # La prioridad es solamente la estimación del vecino.
                heapq.heappush(
                    cola_prioridad,
                    (estimacion, vecino, nuevo_camino, valores + [estimacion])
                )

    # --------------------------------------------------------
    # 7. TERMINAR SI NO EXISTE UNA RUTA
    # --------------------------------------------------------
    return None


# ============================================================
# 8. EJECUTAR LA BÚSQUEDA EN CONSOLA
# ============================================================
if __name__ == "__main__":
    print("GBFS: estado inicial A, estado objetivo J\n")
    resultado = gbfs(estado_inicial, estado_objetivo)

    # ========================================================
    # 9. MOSTRAR LA RUTA ENCONTRADA
    # ========================================================
    if resultado:
        ruta, valores = resultado
        print("\nRuta encontrada:", " -> ".join(ruta))
        print("Valores heurísticos:", valores)
        # Este total suma las heurísticas, incluido A; no es un costo
        # real de aristas ni interviene en la selección de estados GBFS.
        print("Costo total (suma de heurísticas):", sum(valores))
    else:
        print("\nNo se encontró una ruta.")
        
        
    