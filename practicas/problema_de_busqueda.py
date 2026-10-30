from collections import deque


#_________________________________"

estados = {"A", "B", "C", "D", "E", "F", "G"}

estado_iniciale = "A"

estado_objetivo = "G"

acciones = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "D", "F"],
    "D": ["B", "C", "G"],
    "E": ["B", "G"],
    "F": ["C", "G"],
    "G": ["D", "E", "F"]
    }

print("Estados:", estados)
print("Estado inicial:", estado_iniciale)
print("Estado objetivo:", estado_objetivo)
print("Acciones:", acciones)

for estado, vecinos in acciones.items():
    print(
        estado,
        "->",
        vecinos
    )
    
    
    
    
def busqueda_bfs(inicial, objetivo):
    
    cola = deque()
    cola.append(
        (inicial, [inicial])
    )
    
    visitados = set()
    
    while cola:
        estado_actual, camino = cola.popleft()
        
        if estado_actual == objetivo:
            return camino
        
        if estado_actual not in visitados:
            
            visitados.add(estado_actual)
            
            for vecino in acciones[estado_actual]:
                if vecino not in visitados:
                    nuevo_camino = camino + [vecino]
                    cola.append(
                        (vecino, nuevo_camino)
                    )
    return None

camino = busqueda_bfs(
    estado_iniciale, 
    estado_objetivo
)

print("\nCamino encontrado:", camino)
print(
    "Numero de movimientos:",
len(camino) - 1
)

