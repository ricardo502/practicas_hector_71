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



import tkinter as tk
from tkinter import ttk

# ============================================================
# 1. ESPACIO DE BÚSQUEDA: CASA, AVENIDAS Y CALLES
# ============================================================
# Cada tupla guarda (vecino, minutos estimados desde ese vecino
# hasta J). Son heurísticas h(n), no tiempos de las conexiones.
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

# A no tiene un padre que almacene su estimación.
estimacion_inicial = 25


# ============================================================
# 2. BÚSQUEDA VORAZ CON HEURÍSTICA
# ============================================================
def busqueda_voraz(inicial="A", objetivo="J"):
    pendientes = [(inicial, [inicial], estimacion_inicial)]
    visitados = set()
    pasos = []

    while pendientes:
        # Elegir el pendiente con menor tiempo estimado restante.
        pendientes.sort(key=lambda elemento: elemento[2])
        actual, camino, estimacion = pendientes.pop(0)
        if actual in visitados:
            continue
        visitados.add(actual)

        if actual != objetivo:
            for vecino, minutos in grafo[actual]:
                if vecino not in visitados:
                    pendientes.append((vecino, camino + [vecino], minutos))

        # Guardar cada paso para mostrarlo después en la ventana.
        frontera = sorted(
            [(nodo, minutos) for nodo, _, minutos in pendientes
             if nodo not in visitados],
            key=lambda elemento: elemento[1]
        )
        pasos.append((actual, camino.copy(), estimacion, frontera))
        if actual == objetivo:
            return camino, pasos

    return None, pasos


# ============================================================
# 3. VENTANA Y DIBUJO DEL GRAFO CON TKINTER
# ============================================================
class VentanaRecorrido:
    def __init__(self, ventana):
        self.ventana = ventana
        ventana.title("Ruta")
        ventana.geometry("960x800")
        self.temporizador = None
        self.ruta, self.pasos = busqueda_voraz()
        self.indice = 0
        self.posiciones = {
            "A": (450, 55), "B": (240, 155), "C": (660, 155),
            "D": (130, 255), "E": (350, 255),
            "F": (560, 255), "G": (780, 255),
            "H": (130, 355), "I": (560, 355), "J": (660, 455)
        }
        self.estimaciones = {"A": estimacion_inicial}
        for vecinos in grafo.values():
            for vecino, minutos in vecinos:
                self.estimaciones[vecino] = minutos

        ttk.Label(ventana, text="Ruta de casa A al destino J Universidad",
                  font=("Arial", 17, "bold")).pack(pady=8)
        
        self.lienzo = tk.Canvas(ventana, width=900, height=515,
                               bg="#f7fafc", highlightthickness=0)
        self.lienzo.pack(pady=8)
        controles = ttk.Frame(ventana)
        controles.pack()
        # Antes había tres botones: Animar iniciaba la animación,
        # Siguiente paso avanzaba un nodo y Reiniciar limpiaba el dibujo.
        # Ahora un solo botón reinicia y realiza todo el recorrido.
        ttk.Button(controles, text="Hacer recorrido", command=self.animar).pack(padx=6)
        self.estado = tk.StringVar()
        ttk.Label(ventana, textvariable=self.estado, wraplength=900,
                  justify="center", font=("Arial", 11)).pack(pady=10)
       
        self.dibujar([], [])
        self.estado.set("Pulsa Hacer recorrido para comenzar en A (25 min).")
        ventana.protocol("WM_DELETE_WINDOW", self.cerrar)

    def dibujar(self, camino, frontera):
        self.lienzo.delete("all")
        conexiones = set(zip(camino, camino[1:]))
        for padre, vecinos in grafo.items():
            for hijo, _ in vecinos:
                x1, y1 = self.posiciones[padre]
                x2, y2 = self.posiciones[hijo]
                activo = (padre, hijo) in conexiones
                self.lienzo.create_line(x1, y1 + 24, x2, y2 - 24,
                                        arrow=tk.LAST, width=4 if activo else 2,
                                        fill="#2563eb" if activo else "#94a3b8")
        for nodo, (x, y) in self.posiciones.items():
            color = "#ffffff"
            # Solo se colorean los nodos del camino recorrido.
            if nodo in camino:
                color = "#93c5fd"
            if nodo == "J" and nodo in camino:
                color = "#86efac"
            self.lienzo.create_oval(x-25, y-25, x+25, y+25,
                                    fill=color, outline="#334155", width=2)
            self.lienzo.create_text(x, y, text=nodo, font=("Arial", 14, "bold"))
            tipo = "Casa" if nodo == "A" else "Destino" if nodo == "J" else "Avenida" if nodo in "BC" else "Calle"
            self.lienzo.create_text(x, y+40,
                                    text=f"{tipo} · h={self.estimaciones[nodo]} min",
                                    font=("Arial", 10))
            if nodo in ("E", "G", "H"):
                self.lienzo.create_text(x, y+57, text="Sin conexiones de salida",
                                        font=("Arial", 9), fill="#64748b")

    # ========================================================
    # 4. MOSTRAR CADA PASO Y LA RUTA ENCONTRADA
    # ========================================================
    def avanzar(self):
        if self.indice >= len(self.pasos):
            return
        actual, camino, minutos, frontera = self.pasos[self.indice]
        self.indice += 1
        self.dibujar(camino, frontera)
        if actual == "J":
            self.estado.set("Llegaste: " + " → ".join(camino) +
                            ". En J quedan 0 minutos estimados. "
                            "Para calcular la duración real se necesitan los tiempos de cada conexión.")
        else:
            self.estado.set(f"Visitando {actual}: h={minutos} min.\n"
                            "Recorrido: " + " → ".join(camino))
            if self.indice == len(self.pasos) and self.ruta is None:
                self.estado.set("No se encontró una ruta hasta J.")

    def animar(self):
        # Cada clic comienza desde A; cancela cualquier animación anterior.
        self.reiniciar()
        self.tick()

    def tick(self):
        # after programa el siguiente paso sin bloquear la ventana.
        self.temporizador = None
        self.avanzar()
        if self.indice < len(self.pasos):
            self.temporizador = self.ventana.after(1200, self.tick)

    def detener(self):
        if self.temporizador is not None:
            self.ventana.after_cancel(self.temporizador)
            self.temporizador = None

    def reiniciar(self):
        self.detener()
        self.indice = 0
        self.dibujar([], [])
        self.estado.set("Comenzamos en casa A: h(A)=25 min.")

    def cerrar(self):
        self.detener()
        self.ventana.destroy()


# ============================================================
# 5. EJECUTAR LA APLICACIÓN
# ============================================================
if __name__ == "__main__":
    raiz = tk.Tk()
    VentanaRecorrido(raiz)
    raiz.mainloop()
