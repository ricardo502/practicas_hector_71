import itertools
import math
import tkinter as tk
from tkinter import ttk, messagebox

# Coordenadas del ejercicio
PUNTOS = {
    'Almacén': (0, 0),
    'A': (2, 6),
    'B': (5, 3),
    'C': (6, 8),
    'D': (8, 2),
    'E': (1, 1),
}
CLIENTES = ('A', 'B', 'C', 'D', 'E')


def distancia(a, b):
    x1, y1 = PUNTOS[a]
    x2, y2 = PUNTOS[b]
    return math.hypot(x2 - x1, y2 - y1)


def calcular_ruta(orden):
    recorrido = ('Almacén',) + tuple(orden) + ('Almacén',)
    tramos = [(a, b, distancia(a, b)) for a, b in zip(recorrido, recorrido[1:])]
    return recorrido, tramos, sum(t[2] for t in tramos)


class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Algoritmos genéticos — 120 rutas del robot')
        self.geometry('1200x740')
        self.minsize(920, 580)
        self.configure(bg='#edf2f7')

        self.rutas = []
        self.datos_por_id = {}
        self.crear_interfaz()
        self.generar_combinaciones()

    def crear_interfaz(self):
        cabecera = tk.Frame(self, bg='#15314e', padx=16, pady=12)
        cabecera.pack(fill='x')
        tk.Label(cabecera, text='Optimización de rutas — 5 clientes',
                 bg='#15314e', fg='white', font=('Arial', 19, 'bold')).pack(anchor='w')
        tk.Label(cabecera, text='Almacén (0,0)  |  Visita cada cliente una vez  |  Regresa al almacén',
                 bg='#15314e', fg='#cee3f3', font=('Arial', 10)).pack(anchor='w')

        principal = tk.PanedWindow(self, orient='horizontal', sashwidth=6, bg='#dbe4ed')
        principal.pack(fill='both', expand=True, padx=12, pady=12)

        izquierda = tk.Frame(principal, bg='white', padx=12, pady=12)
        derecha = tk.Frame(principal, bg='white', padx=12, pady=12)
        principal.add(izquierda, minsize=350, width=510)
        principal.add(derecha, minsize=390)

        tk.Label(izquierda, text='120 combinaciones (5! = 120)',
                 font=('Arial', 14, 'bold'), bg='white', fg='#163047').pack(anchor='w')
        tk.Label(izquierda, text='Haz clic en una fila para dibujar su recorrido.',
                 bg='white', fg='#536274').pack(anchor='w', pady=(2, 10))

        tabla_frame = tk.Frame(izquierda, bg='white')
        tabla_frame.pack(fill='both', expand=True)
        columnas = ('num', 'ruta', 'costo')
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show='headings', selectmode='browse')
        self.tabla.heading('num', text='#')
        self.tabla.heading('ruta', text='Orden de clientes')
        self.tabla.heading('costo', text='Costo total')
        self.tabla.column('num', width=48, anchor='center', stretch=False)
        self.tabla.column('ruta', width=265, anchor='center')
        self.tabla.column('costo', width=95, anchor='e', stretch=False)
        scrollbar = ttk.Scrollbar(tabla_frame, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        self.tabla.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.tabla.bind('<<TreeviewSelect>>', self.seleccionar_ruta)
        self.tabla.tag_configure('mejor', background='#d7f5e2')

        acciones = tk.Frame(izquierda, bg='white')
        acciones.pack(fill='x', pady=(12, 0))
        ttk.Button(acciones, text='Ordenar por menor costo', command=self.ordenar_por_costo).pack(side='left', padx=(0, 7))
        ttk.Button(acciones, text='Orden A-Z', command=self.ordenar_alfabetico).pack(side='left')

        self.resumen = tk.Label(izquierda, bg='white', fg='#087d53',
                                font=('Arial', 11, 'bold'), justify='left')
        self.resumen.pack(anchor='w', pady=(12, 0))

        tk.Label(derecha, text='Gráfica del recorrido', font=('Arial', 14, 'bold'),
                 bg='white', fg='#163047').pack(anchor='w')
        self.canvas = tk.Canvas(derecha, bg='#fbfdff', highlightthickness=1,
                                highlightbackground='#c5d5e3')
        self.canvas.pack(fill='both', expand=True, pady=(10, 8))
        self.canvas.bind('<Configure>', lambda event: self.refrescar_grafica())

        self.nombre_ruta = tk.Label(derecha, bg='white', fg='#1a3b59',
                                    font=('Arial', 11, 'bold'), wraplength=530, justify='left')
        self.nombre_ruta.pack(anchor='w')
        self.detalle = tk.Label(derecha, bg='white', fg='#475569',
                                font=('Arial', 10), justify='left')
        self.detalle.pack(anchor='w', pady=(5, 0))

    def generar_combinaciones(self):
        self.rutas = []
        for orden in itertools.permutations(CLIENTES):
            recorrido, tramos, costo = calcular_ruta(orden)
            self.rutas.append({'orden': orden, 'recorrido': recorrido,
                               'tramos': tramos, 'costo': costo})
        self.mejor_costo = min(r['costo'] for r in self.rutas)
        mejores = sum(math.isclose(r['costo'], self.mejor_costo, abs_tol=1e-9)
                      for r in self.rutas)
        self.resumen.config(text=f'Total: {len(self.rutas)} rutas  |  Mínimo: {self.mejor_costo:.2f} unidades\n'
                                 f'Rutas con costo mínimo: {mejores}')
        self.mostrar_tabla(self.rutas)

    def mostrar_tabla(self, rutas):
        self.tabla.delete(*self.tabla.get_children())
        self.datos_por_id.clear()
        for numero, ruta in enumerate(rutas, 1):
            es_mejor = math.isclose(ruta['costo'], self.mejor_costo, abs_tol=1e-9)
            iid = str(numero)
            self.datos_por_id[iid] = ruta
            self.tabla.insert('', 'end', iid=iid,
                              values=(numero, ' → '.join(ruta['orden']), f"{ruta['costo']:.2f}"),
                              tags=('mejor',) if es_mejor else ())
        primero = self.tabla.get_children()[0]
        self.tabla.selection_set(primero)
        self.tabla.see(primero)
        self.seleccionar_ruta()

    def ordenar_por_costo(self):
        self.mostrar_tabla(sorted(self.rutas, key=lambda r: (r['costo'], r['orden'])))

    def ordenar_alfabetico(self):
        self.mostrar_tabla(sorted(self.rutas, key=lambda r: r['orden']))

    def seleccionar_ruta(self, event=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        self.actual = self.datos_por_id[seleccion[0]]
        ruta = self.actual
        self.nombre_ruta.config(text=' → '.join(ruta['recorrido']))
        detalle_tramos = '   |   '.join(f'{a}→{b}: {d:.2f}' for a, b, d in ruta['tramos'])
        self.detalle.config(text=f"Costo (fitness): {ruta['costo']:.2f} unidades\n{detalle_tramos}",
                            wraplength=max(self.canvas.winfo_width() - 10, 350))
        self.refrescar_grafica()

    def refrescar_grafica(self):
        if not hasattr(self, 'actual'):
            return
        c = self.canvas
        c.delete('all')
        w = c.winfo_width()
        h = c.winfo_height()
        if w < 80 or h < 80:
            return
        margen = 45
        escala = min((w - 2 * margen) / 9, (h - 2 * margen) / 9)
        origen_x = (w - 9 * escala) / 2
        origen_y = (h + 9 * escala) / 2

        def xy(punto):
            x, y = PUNTOS[punto]
            return origen_x + x * escala, origen_y - y * escala

        for i in range(10):
            x = origen_x + i * escala
            y = origen_y - i * escala
            c.create_line(x, origen_y, x, origen_y - 9 * escala, fill='#e1eaf2')
            c.create_line(origen_x, y, origen_x + 9 * escala, y, fill='#e1eaf2')
            c.create_text(x, origen_y + 15, text=str(i), fill='#516175', font=('Arial', 9))
            c.create_text(origen_x - 16, y, text=str(i), fill='#516175', font=('Arial', 9))
        c.create_line(origen_x, origen_y, origen_x + 9 * escala + 8, origen_y,
                      arrow='last', fill='#657c94', width=2)
        c.create_line(origen_x, origen_y, origen_x, origen_y - 9 * escala - 8,
                      arrow='last', fill='#657c94', width=2)

        for a, b, _ in self.actual['tramos']:
            x1, y1 = xy(a)
            x2, y2 = xy(b)
            c.create_line(x1, y1, x2, y2, fill='#2563eb', width=2.5,
                          arrow='last', arrowshape=(10, 12, 4))
        for punto in PUNTOS:
            x, y = xy(punto)
            color = '#ef4444' if punto == 'Almacén' else '#0d9488'
            r = 7
            c.create_oval(x-r, y-r, x+r, y+r, fill=color, outline='white', width=2)
            etiqueta = 'Almacén' if punto == 'Almacén' else punto
            dx = 34 if punto == 'Almacén' else 0
            dy = -18 if punto == 'Almacén' else -16
            c.create_text(x+dx, y+dy, text=etiqueta, fill='#0f172a',
                          font=('Arial', 10, 'bold'))


if __name__ == '__main__':
    app = Aplicacion()
    app.mainloop()
