# ================================================================
# COMPARATIVO DE ALGORITMOS DE BUSQUEDA
# BFS, DFS, UCS, GREEDY BEST-FIRST SEARCH y A*
# Interfaz grafica con Tkinter
#
# Requisitos:
#   Python 3 instalado.
#   Tkinter normalmente viene incluido con Python.
#
# Ejecucion:
#   Dependerá de como este configurado su WSL: p30algoritmosbusquedacompara.py
#
# Objetivo didactico:
#   Comparar cinco algoritmos sobre el mismo grafo, con el mismo
#   origen y destino, mostrando rutas, costos y nodos expandidos.
# ================================================================

import tkinter as tk
from tkinter import ttk, messagebox
import heapq
from collections import deque
import math


# ------------------------------------------------
# 1. DEFINICION DEL GRAFO
# ------------------------------------------------
# Cada conexion tiene un costo positivo.
# Ejemplo: "A": {"B": 2, "C": 5}
# significa que ir de A a B cuesta 2 y de A a C cuesta 5.
#
# El grafo es dirigido: si A conecta con B, no significa
# automaticamente que B conecte con A.
# ------------------------------------------------

GRAFO = {
    "A": {"B": 2, "C": 5},
    "B": {"D": 4, "E": 7},
    "C": {"F": 2, "G": 6},
    "D": {"H": 3},
    "E": {"H": 2},
    "F": {"I": 3},
    "G": {"I": 2},
    "H": {"J": 5},
    "I": {"J": 2},
    "J": {}
}

# ------------------------------------------------
# 2. HEURISTICA
# ------------------------------------------------
# h(n) estima el costo que falta desde el nodo n hasta J.
# Para demostrar la comparacion, estos valores son ilustrativos.
# En un problema real deben estimarse con informacion del dominio.
#
# Nota: una heuristica arbitraria puede hacer que A* no garantice
# la ruta optima. Para este ejemplo, se usa una heuristica admisible
# respecto a los costos del grafo: no sobreestima el costo restante.
# ------------------------------------------------

HEURISTICA_HASTA_J = {
    "A": 9,
    "B": 8,
    "C": 5,
    "D": 6,
    "E": 5,
    "F": 4,
    "G": 3,
    "H": 5,
    "I": 2,
    "J": 0
}

# Posiciones de cada nodo en el lienzo de Tkinter.
POSICIONES = {
    "A": (350, 55),
    "B": (220, 145),
    "C": (480, 145),
    "D": (130, 240),
    "E": (270, 240),
    "F": (430, 240),
    "G": (570, 240),
    "H": (210, 340),
    "I": (490, 340),
    "J": (350, 440)
}

# Colores para distinguir los estados de los nodos.
COLOR_NORMAL = "#DCEBFA"
COLOR_INICIO = "#35B56A"
COLOR_OBJETIVO = "#E85D5D"
COLOR_EXPANDIDO = "#FFD166"
COLOR_RUTA = "#B9A0F5"
COLOR_FRONTERA = "#8ED8E8"


# ------------------------------------------------
# 3. FUNCIONES AUXILIARES
# ------------------------------------------------

def reconstruir_camino(padres, inicio, objetivo):
    """Reconstruye el camino desde el origen al objetivo."""
    if objetivo != inicio and objetivo not in padres:
        return []

    camino = []
    actual = objetivo

    while actual is not None:
        camino.append(actual)
        if actual == inicio:
            break
        actual = padres.get(actual)

    camino.reverse()

    # Si no se llego al origen, no existe un camino valido.
    if not camino or camino[0] != inicio:
        return []

    return camino


def calcular_costo(camino):
    """Suma los pesos de las aristas que componen un camino."""
    if not camino:
        return math.inf

    costo = 0
    for i in range(len(camino) - 1):
        origen = camino[i]
        destino = camino[i + 1]
        costo += GRAFO[origen][destino]

    return costo


def vecinos_ordenados(nodo):
    """Devuelve vecinos en orden alfabetico para resultados reproducibles."""
    return sorted(GRAFO[nodo].items())


# ------------------------------------------------
# 4. BFS: BUSQUEDA EN ANCHURA
# ------------------------------------------------
# BFS explora primero los nodos mas cercanos al origen en numero
# de aristas. Encuentra una ruta con el menor numero de aristas
# cuando todas las aristas se consideran con el mismo costo.
#
# IMPORTANTE:
# Si las aristas tienen pesos distintos, BFS no garantiza el
# menor costo total. Por eso informamos por separado pasos y costo.
# ------------------------------------------------

def bfs(inicio, objetivo):
    frontera = deque([inicio])
    descubiertos = {inicio}
    padres = {inicio: None}
    expandidos = []
    registro = []

    while frontera:
        actual = frontera.popleft()
        expandidos.append(actual)
        registro.append(f"BFS: se extrae {actual} de la cola.")

        if actual == objetivo:
            break

        for vecino, peso in vecinos_ordenados(actual):
            if vecino not in descubiertos:
                descubiertos.add(vecino)
                padres[vecino] = actual
                frontera.append(vecino)
                registro.append(
                    f"  Se descubre {vecino} desde {actual} "
                    f"(peso de arista={peso})."
                )

    camino = reconstruir_camino(padres, inicio, objetivo)
    return crear_resultado("BFS", camino, expandidos, registro)


# ------------------------------------------------
# 5. DFS: BUSQUEDA EN PROFUNDIDAD
# ------------------------------------------------
# DFS profundiza por una rama antes de explorar las demas.
# El orden depende del orden en que se visitan los vecinos.
# No garantiza la ruta mas corta ni el menor costo.
# ------------------------------------------------

def dfs(inicio, objetivo):
    pila = [inicio]
    descubiertos = {inicio}
    padres = {inicio: None}
    expandidos = []
    registro = []

    while pila:
        actual = pila.pop()
        expandidos.append(actual)
        registro.append(f"DFS: se extrae {actual} de la pila.")

        if actual == objetivo:
            break

        # Se invierte para que el vecino alfabeticamente primero
        # sea el primero en salir de la pila.
        for vecino, peso in reversed(vecinos_ordenados(actual)):
            if vecino not in descubiertos:
                descubiertos.add(vecino)
                padres[vecino] = actual
                pila.append(vecino)
                registro.append(
                    f"  Se agrega {vecino} a la pila desde {actual} "
                    f"(peso={peso})."
                )

    camino = reconstruir_camino(padres, inicio, objetivo)
    return crear_resultado("DFS", camino, expandidos, registro)


# ------------------------------------------------
# 6. UCS: BUSQUEDA DE COSTO UNIFORME
# ------------------------------------------------
# UCS expande el nodo con menor costo real acumulado g(n).
# Con pesos no negativos, encuentra una ruta de costo minimo.
# ------------------------------------------------

def ucs(inicio, objetivo):
    frontera = [(0, inicio)]
    mejor_costo = {inicio: 0}
    padres = {inicio: None}
    expandidos = []
    registro = []
    cerrados = set()

    while frontera:
        costo_actual, actual = heapq.heappop(frontera)

        # Ignorar entradas antiguas que ya no tienen el mejor costo.
        if costo_actual != mejor_costo.get(actual, math.inf):
            continue

        if actual in cerrados:
            continue

        cerrados.add(actual)
        expandidos.append(actual)
        registro.append(
            f"UCS: se expande {actual} con g(n)={costo_actual}."
        )

        if actual == objetivo:
            break

        for vecino, peso in vecinos_ordenados(actual):
            nuevo_costo = costo_actual + peso

            if nuevo_costo < mejor_costo.get(vecino, math.inf):
                mejor_costo[vecino] = nuevo_costo
                padres[vecino] = actual
                heapq.heappush(frontera, (nuevo_costo, vecino))
                registro.append(
                    f"  Mejor costo para {vecino}: g(n)={nuevo_costo}."
                )

    camino = reconstruir_camino(padres, inicio, objetivo)
    return crear_resultado("UCS", camino, expandidos, registro)


# ------------------------------------------------
# 7. GREEDY BEST-FIRST SEARCH: BUSQUEDA VORAZ
# ------------------------------------------------
# Greedy selecciona el nodo con menor h(n), es decir, el que
# parece mas cercano al objetivo segun la heuristica.
#
# No toma en cuenta el costo real acumulado para decidir.
# Por ello puede encontrar una ruta no optima.
# ------------------------------------------------

def greedy(inicio, objetivo, heuristica):
    frontera = [(heuristica[inicio], inicio)]
    descubiertos = {inicio}
    padres = {inicio: None}
    expandidos = []
    registro = []

    while frontera:
        h_actual, actual = heapq.heappop(frontera)
        expandidos.append(actual)
        registro.append(
            f"Greedy: se expande {actual} con h(n)={h_actual}."
        )

        if actual == objetivo:
            break

        for vecino, peso in vecinos_ordenados(actual):
            if vecino not in descubiertos:
                descubiertos.add(vecino)
                padres[vecino] = actual
                heapq.heappush(
                    frontera, (heuristica[vecino], vecino)
                )
                registro.append(
                    f"  Se agrega {vecino}: h(n)={heuristica[vecino]}."
                )

    camino = reconstruir_camino(padres, inicio, objetivo)
    return crear_resultado("Greedy", camino, expandidos, registro)


# ------------------------------------------------
# 8. A*: g(n) + h(n)
# ------------------------------------------------
# A* combina:
#   g(n): costo real desde el origen.
#   h(n): estimacion del costo restante.
#   f(n) = g(n) + h(n): costo estimado total.
#
# Con costos no negativos y una heuristica admisible, A* en grafo
# con reapertura de nodos cuando mejora g puede encontrar una
# ruta optima.
# ------------------------------------------------

def astar(inicio, objetivo, heuristica):
    frontera = [(heuristica[inicio], 0, inicio)]
    mejor_g = {inicio: 0}
    padres = {inicio: None}
    expandidos = []
    registro = []

    while frontera:
        f_actual, g_actual, actual = heapq.heappop(frontera)

        # Ignorar una entrada desactualizada.
        if g_actual != mejor_g.get(actual, math.inf):
            continue

        expandidos.append(actual)
        registro.append(
            f"A*: se expande {actual}: "
            f"g(n)={g_actual}, h(n)={heuristica[actual]}, "
            f"f(n)={f_actual}."
        )

        if actual == objetivo:
            break

        for vecino, peso in vecinos_ordenados(actual):
            nuevo_g = g_actual + peso

            if nuevo_g < mejor_g.get(vecino, math.inf):
                mejor_g[vecino] = nuevo_g
                padres[vecino] = actual
                nuevo_f = nuevo_g + heuristica[vecino]
                heapq.heappush(
                    frontera, (nuevo_f, nuevo_g, vecino)
                )
                registro.append(
                    f"  Se actualiza {vecino}: "
                    f"g={nuevo_g}, h={heuristica[vecino]}, "
                    f"f={nuevo_f}."
                )

    camino = reconstruir_camino(padres, inicio, objetivo)
    return crear_resultado("A*", camino, expandidos, registro)


# ------------------------------------------------
# 9. FORMATO COMUN DE RESULTADOS
# ------------------------------------------------
# Todos los algoritmos entregan la misma estructura de datos.
# Esto facilita compararlos sin mezclar sus implementaciones.
# ------------------------------------------------

def crear_resultado(nombre, camino, expandidos, registro):
    return {
        "algoritmo": nombre,
        "camino": camino,
        "costo": calcular_costo(camino) if camino else math.inf,
        "pasos": len(camino) - 1 if camino else 0,
        "expandidos": expandidos,
        "cantidad_expandidos": len(expandidos),
        "registro": registro
    }


ALGORITMOS = {
    "BFS": bfs,
    "DFS": dfs,
    "UCS": ucs,
    "Greedy": greedy,
    "A*": astar
}


# ------------------------------------------------
# 10. INTERFAZ GRAFICA
# ------------------------------------------------

class LaboratorioBusqueda:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title(
            "Laboratorio de Busqueda IA | BFS, DFS, UCS, Greedy y A*"
        )
        self.ventana.geometry("1120x850")
        self.ventana.minsize(900, 800)

        self.inicio = "A"
        self.objetivo = "J"
        self.resultados = {}
        self.modo_seleccion = tk.StringVar(value="Inicio")

        self.construir_interfaz()
        self.dibujar_grafo()
        self.mostrar_instrucciones()

    def construir_interfaz(self):
        # Encabezado
        encabezado = ttk.Frame(self.ventana, padding=10)
        encabezado.pack(fill="x")

        ttk.Label(
            encabezado,
            text="LABORATORIO DE ALGORITMOS DE BUSQUEDA",
            font=("Arial", 16, "bold")
        ).pack(anchor="w")

        ttk.Label(
            encabezado,
            text=(
                "Selecciona origen y destino, ejecuta un algoritmo "
                "o compara los cinco sobre el mismo grafo."
            )
        ).pack(anchor="w", pady=(4, 0))

        # Controles de selección
        controles = ttk.LabelFrame(
            self.ventana, text="Configuracion de la busqueda", padding=8
        )
        controles.pack(fill="x", padx=10, pady=5)

        ttk.Label(controles, text="Nodo inicial:").grid(
            row=0, column=0, padx=5, pady=4, sticky="w"
        )
        self.combo_inicio = ttk.Combobox(
            controles, values=list(GRAFO.keys()), state="readonly", width=8
        )
        self.combo_inicio.set(self.inicio)
        self.combo_inicio.grid(row=0, column=1, padx=5, pady=4)
        self.combo_inicio.bind(
            "<<ComboboxSelected>>", self.cambiar_inicio
        )

        ttk.Label(controles, text="Nodo objetivo:").grid(
            row=0, column=2, padx=5, pady=4, sticky="w"
        )
        self.combo_objetivo = ttk.Combobox(
            controles, values=list(GRAFO.keys()), state="readonly", width=8
        )
        self.combo_objetivo.set(self.objetivo)
        self.combo_objetivo.grid(row=0, column=3, padx=5, pady=4)
        self.combo_objetivo.bind(
            "<<ComboboxSelected>>", self.cambiar_objetivo
        )

        ttk.Label(controles, text="Algoritmo:").grid(
            row=0, column=4, padx=5, pady=4, sticky="w"
        )
        self.combo_algoritmo = ttk.Combobox(
            controles,
            values=["BFS", "DFS", "UCS", "Greedy", "A*"],
            state="readonly",
            width=12
        )
        self.combo_algoritmo.set("A*")
        self.combo_algoritmo.grid(row=0, column=5, padx=5, pady=4)

        ttk.Button(
            controles, text="Ejecutar algoritmo",
            command=self.ejecutar_individual
        ).grid(row=0, column=6, padx=5, pady=4)

        ttk.Button(
            controles, text="Comparar los 5",
            command=self.comparar_todos
        ).grid(row=0, column=7, padx=5, pady=4)

        ttk.Button(
            controles, text="Reiniciar vista",
            command=self.reiniciar
        ).grid(row=0, column=8, padx=5, pady=4)

        # Leyenda de colores
        leyenda = ttk.Frame(self.ventana, padding=(10, 2))
        leyenda.pack(fill="x")
        ttk.Label(
            leyenda,
            text="Leyenda: "
        ).pack(side="left")
        for texto, color in [
            ("Inicio", COLOR_INICIO),
            ("Objetivo", COLOR_OBJETIVO),
            ("Expandido", COLOR_EXPANDIDO),
            ("Ruta final", COLOR_RUTA)
        ]:
            muestra = tk.Label(
                leyenda, text=f"  {texto}  ",
                bg=color, relief="groove", padx=3
            )
            muestra.pack(side="left", padx=4)

        # Area principal: grafo a la izquierda y registro a la derecha.
        principal = ttk.Panedwindow(self.ventana, orient="horizontal")
        principal.pack(fill="both", expand=True, padx=10, pady=5)

        marco_grafo = ttk.LabelFrame(
            principal, text="Grafo ponderado", padding=5
        )
        principal.add(marco_grafo, weight=3)

        self.canvas = tk.Canvas(
            marco_grafo, bg="white", width=650, height=500,
            highlightthickness=1, highlightbackground="#BBBBBB"
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.clic_en_grafo)

        ttk.Label(
            marco_grafo,
            text="Tambien puedes hacer clic en un nodo: primero inicio, "
                 "despues objetivo.",
            wraplength=600
        ).pack(anchor="w", pady=(4, 0))

        marco_registro = ttk.LabelFrame(
            principal, text="Registro explicativo", padding=5
        )
        principal.add(marco_registro, weight=2)

        self.registro = tk.Text(
            marco_registro, width=48, height=25,
            wrap="word", font=("Consolas", 9)
        )
        barra = ttk.Scrollbar(
            marco_registro, orient="vertical",
            command=self.registro.yview
        )
        self.registro.configure(yscrollcommand=barra.set)
        self.registro.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        # Tabla comparativa
        marco_tabla = ttk.LabelFrame(
            self.ventana, text="Metricas de resultados", padding=5
        )
        marco_tabla.pack(fill="x", padx=10, pady=(0, 10))

        columnas = (
            "algoritmo", "ruta", "pasos", "costo", "expandidos"
        )
        self.tabla = ttk.Treeview(
            marco_tabla, columns=columnas, show="headings", height=6
        )
        encabezados = {
            "algoritmo": "Algoritmo",
            "ruta": "Ruta encontrada",
            "pasos": "Aristas",
            "costo": "Costo total",
            "expandidos": "Nodos expandidos"
        }
        anchos = {
            "algoritmo": 100, "ruta": 360, "pasos": 80,
            "costo": 100, "expandidos": 140
        }

        for columna in columnas:
            self.tabla.heading(columna, text=encabezados[columna])
            self.tabla.column(
                columna, width=anchos[columna],
                anchor="w" if columna == "ruta" else "center"
            )

        self.tabla.pack(fill="x")

    # ------------------------------------------------
    # 11. DIBUJO DEL GRAFO
    # ------------------------------------------------

    def dibujar_grafo(self, camino=None, expandidos=None):
        camino = camino or []
        expandidos = expandidos or []

        self.canvas.delete("all")

        # Dibujar las aristas antes que los nodos para que queden debajo.
        for origen, vecinos in GRAFO.items():
            x1, y1 = POSICIONES[origen]
            for destino, peso in vecinos.items():
                x2, y2 = POSICIONES[destino]
                en_ruta = (
                    len(camino) > 1 and
                    any(
                        camino[i] == origen and camino[i + 1] == destino
                        for i in range(len(camino) - 1)
                    )
                )

                color = "#7A45C2" if en_ruta else "#9AA3AD"
                grosor = 4 if en_ruta else 2

                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=color, width=grosor,
                    arrow=tk.LAST, arrowshape=(10, 12, 5)
                )

                # Etiqueta del peso, colocada cerca del punto medio.
                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2
                self.canvas.create_rectangle(
                    mx - 12, my - 10, mx + 12, my + 10,
                    fill="white", outline=""
                )
                self.canvas.create_text(
                    mx, my, text=str(peso),
                    fill="#263238", font=("Arial", 9, "bold")
                )

        # Dibujar nodos y sus valores heurísticos.
        for nodo, (x, y) in POSICIONES.items():
            if nodo == self.inicio:
                color = COLOR_INICIO
            elif nodo == self.objetivo:
                color = COLOR_OBJETIVO
            elif nodo in camino:
                color = COLOR_RUTA
            elif nodo in expandidos:
                color = COLOR_EXPANDIDO
            else:
                color = COLOR_NORMAL

            radio = 27
            self.canvas.create_oval(
                x-radio, y-radio, x+radio, y+radio,
                fill=color, outline="#334155", width=2
            )

            # La heuristica mostrada corresponde al objetivo J.
            # Si se cambia el destino, se advierte en la interfaz.
            self.canvas.create_text(
                x, y - 7, text=nodo,
                font=("Arial", 12, "bold")
            )
            self.canvas.create_text(
                x, y + 10,
                text=f"hJ={HEURISTICA_HASTA_J[nodo]}",
                font=("Arial", 8)
            )

        self.canvas.create_text(
            10, 10, anchor="nw",
            text="Aristas = costo | hJ = heuristica estimada hasta J",
            fill="#374151", font=("Arial", 9)
        )

    # ------------------------------------------------
    # 12. SELECCION DE NODOS
    # ------------------------------------------------

    def clic_en_grafo(self, evento):
        x, y = evento.x, evento.y

        for nodo, (nx, ny) in POSICIONES.items():
            if (nx - 30 <= x <= nx + 30 and
                    ny - 30 <= y <= ny + 30):
                if self.modo_seleccion.get() == "Inicio":
                    self.inicio = nodo
                    self.combo_inicio.set(nodo)
                    self.modo_seleccion.set("Objetivo")
                    self.escribir(
                        f"Origen seleccionado: {nodo}. "
                        "Ahora haz clic en el destino."
                    )
                else:
                    self.objetivo = nodo
                    self.combo_objetivo.set(nodo)
                    self.modo_seleccion.set("Inicio")
                    self.escribir(
                        f"Destino seleccionado: {nodo}. "
                        "Puedes ejecutar un algoritmo."
                    )
                self.resultados.clear()
                self.actualizar_tabla()
                self.dibujar_grafo()
                break

    def cambiar_inicio(self, _evento=None):
        self.inicio = self.combo_inicio.get()
        self.limpiar_resultados()

    def cambiar_objetivo(self, _evento=None):
        self.objetivo = self.combo_objetivo.get()
        self.limpiar_resultados()

    def limpiar_resultados(self):
        self.resultados.clear()
        self.actualizar_tabla()
        self.dibujar_grafo()
        self.escribir(
            f"Configuracion actual: {self.inicio} -> {self.objetivo}.\n"
            "Selecciona un algoritmo para comenzar."
        )

    # ------------------------------------------------
    # 13. EJECUCION Y COMPARACION
    # ------------------------------------------------

    def ejecutar_algoritmo(self, nombre):
        if self.inicio == self.objetivo:
            return crear_resultado(
                nombre, [self.inicio], [self.inicio],
                ["El origen y el objetivo son el mismo nodo."]
            )

        if nombre == "BFS":
            return bfs(self.inicio, self.objetivo)
        if nombre == "DFS":
            return dfs(self.inicio, self.objetivo)
        if nombre == "UCS":
            return ucs(self.inicio, self.objetivo)
        if nombre == "Greedy":
            heuristica = self.heuristica_para_objetivo()
            return greedy(self.inicio, self.objetivo, heuristica)
        if nombre == "A*":
            heuristica = self.heuristica_para_objetivo()
            return astar(self.inicio, self.objetivo, heuristica)

        raise ValueError(f"Algoritmo desconocido: {nombre}")

    def heuristica_para_objetivo(self):
        # La heuristica del ejemplo esta definida hasta J.
        # Si el objetivo cambia, no debemos fingir que esos valores
        # siguen siendo una estimacion valida para ese nuevo objetivo.
        if self.objetivo == "J":
            return HEURISTICA_HASTA_J

        # Para otros objetivos usamos h(n)=0, lo que convierte A*
        # en UCS y hace que Greedy pierda la guia heuristica.
        # Es una alternativa segura para permitir cualquier destino.
        return {nodo: 0 for nodo in GRAFO}

    def ejecutar_individual(self):
        nombre = self.combo_algoritmo.get()
        resultado = self.ejecutar_algoritmo(nombre)
        self.resultados = {nombre: resultado}
        self.actualizar_tabla()
        self.dibujar_grafo(
            resultado["camino"], resultado["expandidos"]
        )
        self.mostrar_resultado(resultado)

    def comparar_todos(self):
        self.resultados = {}
        for nombre in ["BFS", "DFS", "UCS", "Greedy", "A*"]:
            self.resultados[nombre] = self.ejecutar_algoritmo(nombre)

        self.actualizar_tabla()

        # Mostrar el camino de A* como referencia en el mapa.
        resultado_astar = self.resultados["A*"]
        self.dibujar_grafo(
            resultado_astar["camino"], resultado_astar["expandidos"]
        )

        self.registro.delete("1.0", tk.END)
        self.registro.insert(
            tk.END,
            f"COMPARACION: {self.inicio} -> {self.objetivo}\n"
            + "=" * 42 + "\n\n"
        )

        for nombre, resultado in self.resultados.items():
            ruta = (
                " -> ".join(resultado["camino"])
                if resultado["camino"] else "Sin ruta"
            )
            costo = (
                str(resultado["costo"])
                if math.isfinite(resultado["costo"]) else "No disponible"
            )
            self.registro.insert(
                tk.END,
                f"{nombre}\n"
                f"  Ruta: {ruta}\n"
                f"  Costo: {costo}\n"
                f"  Aristas: {resultado['pasos']}\n"
                f"  Nodos expandidos: "
                f"{resultado['cantidad_expandidos']}\n\n"
            )

        self.registro.insert(
            tk.END,
            "INTERPRETACION DIDACTICA\n"
            "BFS prioriza la cantidad de aristas, no su peso.\n"
            "DFS profundiza segun el orden de los vecinos.\n"
            "UCS prioriza el costo acumulado g(n).\n"
            "Greedy prioriza la heuristica h(n).\n"
            "A* prioriza f(n)=g(n)+h(n).\n\n"
            "Los nodos expandidos dependen del orden de vecinos y "
            "de la estrategia de cada algoritmo.\n"
        )

    # ------------------------------------------------
    # 14. TABLA Y MENSAJES
    # ------------------------------------------------

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        orden = ["BFS", "DFS", "UCS", "Greedy", "A*"]
        for nombre in orden:
            if nombre not in self.resultados:
                continue

            r = self.resultados[nombre]
            ruta = " -> ".join(r["camino"]) if r["camino"] else "Sin ruta"
            costo = (
                f"{r['costo']:.1f}"
                if math.isfinite(r["costo"]) else "—"
            )
            self.tabla.insert(
                "", "end",
                values=(
                    nombre, ruta, r["pasos"], costo,
                    r["cantidad_expandidos"]
                )
            )

    def mostrar_resultado(self, r):
        self.registro.delete("1.0", tk.END)
        self.registro.insert(
            tk.END,
            f"ALGORITMO: {r['algoritmo']}\n"
            f"ORIGEN: {self.inicio}\n"
            f"OBJETIVO: {self.objetivo}\n"
            + "=" * 42 + "\n\n"
        )

        for linea in r["registro"]:
            self.registro.insert(tk.END, linea + "\n")

        self.registro.insert(tk.END, "\nRESULTADO FINAL\n")
        if r["camino"]:
            self.registro.insert(
                tk.END,
                f"Ruta: {' -> '.join(r['camino'])}\n"
                f"Costo total: {r['costo']}\n"
                f"Numero de aristas: {r['pasos']}\n"
                f"Nodos expandidos: {r['cantidad_expandidos']}\n"
            )
        else:
            self.registro.insert(
                tk.END, "No se encontro una ruta al objetivo.\n"
            )

    def mostrar_instrucciones(self):
        self.escribir(
            "INSTRUCCIONES\n"
            "1. Selecciona origen y destino con los desplegables "
            "o haciendo clic en el grafo.\n"
            "2. Elige un algoritmo y pulsa Ejecutar algoritmo.\n"
            "3. Pulsa Comparar los 5 para ejecutar todos con la "
            "misma configuracion.\n\n"
            "Cada numero junto a una conexion representa su costo.\n"
            "hJ es la heuristica de referencia hacia el nodo J.\n\n"
            "Nota: al seleccionar un objetivo distinto de J, el "
            "programa usa h(n)=0 para Greedy y A*, evitando aplicar "
            "una heuristica que fue definida para otro destino."
        )

    def escribir(self, texto):
        self.registro.insert(tk.END, texto + "\n")
        self.registro.see(tk.END)

    def reiniciar(self):
        self.inicio = "A"
        self.objetivo = "J"
        self.combo_inicio.set(self.inicio)
        self.combo_objetivo.set(self.objetivo)
        self.combo_algoritmo.set("A*")
        self.modo_seleccion.set("Inicio")
        self.resultados.clear()
        self.actualizar_tabla()
        self.dibujar_grafo()
        self.registro.delete("1.0", tk.END)
        self.mostrar_instrucciones()


# ------------------------------------------------
# 15. PUNTO DE ENTRADA DEL PROGRAMA
# ------------------------------------------------

if __name__ == "__main__":
    ventana = tk.Tk()
    app = LaboratorioBusqueda(ventana)
    ventana.mainloop()
