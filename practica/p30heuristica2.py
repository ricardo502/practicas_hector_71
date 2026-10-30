# ============================================================
# EJEMPLO DE BÚSQUEDA HEURÍSTICA EN UNA CIUDAD
# ============================================================
# Objetivo: entender cómo una heurística orienta la búsqueda
# sin ser necesariamente el costo real.
#
# Escenario: queremos ir desde nuestra CASA (A) hasta la UNIVERSIDAD (J).
# El grafo representa calles y conexiones posibles.
# ============================================================

# ------------------------------------------------------------
# 1. ESPACIO DE ESTADOS (Calles y conexiones)
# ------------------------------------------------------------
ciudad = {
    "A": ["B", "C"],   # Casa conecta con dos avenidas
    "B": ["D", "E"],   # Avenida B conecta con dos calles
    "C": ["F", "G"],   # Avenida C conecta con otras dos
    "D": ["H"],        # Calle D lleva a H
    "E": [],           # Calle E es calle sin salida
    "F": ["I"],        # Calle F lleva a I
    "G": [],           # Calle G es calle sin salida
    "H": [],           # Calle H es calle sin salida
    "I": ["J"],        # Calle I conecta directo a la universidad
    "J": []            # Universidad (objetivo)
}

# ------------------------------------------------------------
# 2. HEURÍSTICA (Estimación en minutos caminando)
# ------------------------------------------------------------
# IMPORTANTE:
# Estos valores NO son el tiempo real, solo una estimación
# que nos ayuda a decidir qué camino parece más prometedor.
# ------------------------------------------------------------
h = {
    "A": 25,   # Desde casa calculo 25 min
    "B": 20,
    "C": 15,
    "D": 18,
    "E": 30,   # Parece buena opción, pero es calle sin salida
    "F": 10,
    "G": 25,
    "H": 40,   # Muy lejos y sin salida
    "I": 5,
    "J": 0     # Ya estamos en la universidad
}

# ------------------------------------------------------------
# 3. FUNCIÓN DE BÚSQUEDA HEURÍSTICA SIMPLE
# ------------------------------------------------------------
def busqueda_heuristica(inicio, objetivo):
    # Estado actual
    actual = inicio

    # Camino recorrido
    camino = [actual]

    # Estados visitados
    visitados = set()

    # Comenzamos la búsqueda
    while actual != objetivo:
        # Marcar estado como visitado
        visitados.add(actual)

        print(f"\n Estado actual: {actual} | h({actual}) = {h[actual]} min")

        # Obtener vecinos disponibles
        candidatos = [v for v in ciudad[actual] if v not in visitados]

        # Si no hay opciones, terminamos
        if not candidatos:
            print(" No hay más caminos disponibles.")
            return None

        # Seleccionar vecino con menor heurística
        siguiente = min(candidatos, key=lambda x: h[x])
        print(f" Avanzamos hacia: {siguiente} (h={h[siguiente]} min)")

        # Avanzamos
        actual = siguiente
        camino.append(actual)

    # Objetivo encontrado
    print("\n OBJETIVO ENCONTRADO: Universidad")
    return camino

# ------------------------------------------------------------
# 4. EJECUTAR
# ------------------------------------------------------------
ruta = busqueda_heuristica("A", "J")

# ------------------------------------------------------------
# 5. MOSTRAR RESULTADO
# ------------------------------------------------------------
print("\n==============================")
print(" RUTA RESULTANTE")
print("==============================")
if ruta:
    print(" → ".join(ruta))
else:
    print("No se encontró solución.")
