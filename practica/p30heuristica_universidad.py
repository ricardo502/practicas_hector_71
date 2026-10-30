# Busqueda heuristica basada en p30heuristica2.py.
# Ejemplo ilustrativo: recorrido desde Casa hasta Universidad.
# Los lugares y los minutos no corresponden a un mapa real.

# 1. ESPACIO DE ESTADOS
# Cada estado es un lugar donde podemos estar durante el recorrido.
estados = (
    "Casa", "Parque", "Mercado", "AvenidaPrincipal",
    "ParadaAutobus", "Puente", "Hospital", "Universidad",
)
inicio = "Casa"
objetivo = "Universidad"

# 2. PUNTOS O NODOS DEL GRAFO
# Se usan nombres sin espacios ni puntos para identificar los estados.
# Casa ---- Parque ---- AvenidaPrincipal ---- Puente ---- Universidad
#   |                      |                                |
# Mercado ----------- ParadaAutobus ------------------ Hospital

# 3. GRAFO
# Las conexiones permiten recorrer los caminos en ambos sentidos.
grafo = {
    "Casa": ["Parque", "Mercado"],
    "Parque": ["Casa", "AvenidaPrincipal"],
    "Mercado": ["Casa", "ParadaAutobus"],
    "AvenidaPrincipal": ["Parque", "ParadaAutobus", "Puente"],
    "ParadaAutobus": ["Mercado", "AvenidaPrincipal", "Hospital"],
    "Puente": ["AvenidaPrincipal", "Universidad"],
    "Hospital": ["ParadaAutobus", "Universidad"],
    "Universidad": ["Puente", "Hospital"],
}

# 4. HEURISTICA HACIA LA UNIVERSIDAD
# h(n) estima cuantos minutos faltan desde cada lugar al objetivo.
# No representa el costo de una conexion ni el tiempo total de la ruta.
h = {
    "Casa": 30,
    "Parque": 22,
    "Mercado": 26,
    "AvenidaPrincipal": 14,
    "ParadaAutobus": 18,
    "Puente": 6,
    "Hospital": 9,
    "Universidad": 0,
}


# 5. BUSQUEDA HEURISTICA SIMPLE
# Conserva la regla del original: avanzar al vecino no visitado con
# menor h(n). No retrocede ni garantiza encontrar la ruta mas corta.
def busqueda_heuristica(inicio, objetivo):
    actual = inicio
    camino = [actual]
    visitados = set()

    while actual != objetivo:
        visitados.add(actual)
        print(f"\nEstado actual: {actual} | h({actual}) = {h[actual]} min")
        candidatos = [v for v in grafo[actual] if v not in visitados]

        if not candidatos:
            print("No hay mas caminos disponibles desde este estado.")
            return None

        siguiente = min(candidatos, key=lambda estado: h[estado])
        print(f"Avanzamos hacia: {siguiente} (h={h[siguiente]} min)")
        actual = siguiente
        camino.append(actual)

    print(f"\nOBJETIVO ENCONTRADO: {objetivo} | h = {h[objetivo]} min")
    return camino


if __name__ == "__main__":
    print("ESPACIO DE ESTADOS")
    print(", ".join(estados))
    print("\nHEURISTICA HACIA LA UNIVERSIDAD")
    for estado in estados:
        print(f"{estado}: {h[estado]} min")

    ruta = busqueda_heuristica(inicio, objetivo)
    print("\nRUTA RESULTANTE")
    if ruta:
        print(" -> ".join(ruta))
    else:
        print("No se encontro solucion con esta busqueda.")
