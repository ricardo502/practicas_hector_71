"""Interfaz de escritorio del centro de control."""

import tkinter as tk
from tkinter import messagebox, ttk
from analisis import analizar_flota, tabla_verdad
from decision import evaluar
from vehiculo import Vehiculo


class LogiSmartApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LogiSmart · Centro de control")
        self.geometry("1000x720")
        self.minsize(850, 680)
        self.flota = []
        self.identificador = tk.StringVar()
        self.condiciones = [tk.BooleanVar(value=False) for _ in range(4)]
        self.resultado = tk.StringVar(value="Ingresa un vehículo para conocer su resultado.")
        self.resumen = tk.StringVar()
        marco = ttk.Frame(self, padding=20)
        marco.pack(fill="both", expand=True)
        ttk.Label(marco, text="LogiSmart", font=("Segoe UI", 22, "bold")).pack(anchor="w")
        ttk.Label(marco, text="Centro de control de vehículos").pack(anchor="w", pady=(0, 12))
        pestanas = ttk.Notebook(marco)
        pestanas.pack(fill="both", expand=True)
        control = ttk.Frame(pestanas, padding=12)
        tabla = ttk.Frame(pestanas, padding=12)
        pestanas.add(control, text="Evaluación y flota")
        pestanas.add(tabla, text="Tabla de verdad")
        formulario = ttk.LabelFrame(control, text="Datos del vehículo", padding=12)
        formulario.pack(fill="x")
        ttk.Label(formulario, text="Identificador:").pack(anchor="w")
        self.entrada = ttk.Entry(formulario, textvariable=self.identificador, width=35)
        self.entrada.pack(anchor="w", pady=5)
        etiquetas = ("P · Vehículo autorizado", "Q · Excede el límite de peso",
                     "R · Transporta material peligroso", "S · Conductor con certificación vigente")
        for etiqueta, variable in zip(etiquetas, self.condiciones):
            ttk.Checkbutton(formulario, text=etiqueta, variable=variable).pack(anchor="w", pady=2)
        ttk.Label(formulario, text="Marcado = Sí; sin marcar = No.").pack(anchor="w", pady=5)
        botones = ttk.Frame(formulario)
        botones.pack(anchor="w", pady=5)
        ttk.Button(botones, text="Evaluar y registrar", command=self.registrar).pack(side="left")
        ttk.Button(botones, text="Limpiar formulario", command=self.limpiar).pack(side="left", padx=10)
        ttk.Label(control, textvariable=self.resultado, wraplength=760,
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=10)
        self.registros = self._tabla(control, ("Vehículo", "P", "Q", "R", "S", "Acceso", "Inspección"), 5)
        self.registros.column("Vehículo", width=180)
        ttk.Label(control, textvariable=self.resumen, wraplength=760).pack(anchor="w", pady=8)
        ttk.Label(control, text="Los registros se conservan solo mientras la ventana está abierta.").pack(anchor="w")
        ttk.Label(tabla, text="Acceso: A = P ∧ S ∧ ¬Q     |     Inspección: I = P ∧ (R ∨ Q)").pack(anchor="w", pady=8)
        ttk.Label(tabla, text="1 = verdadero; 0 = falso. Acceso e inspección pueden ocurrir a la vez.").pack(anchor="w", pady=8)
        self.tabla = self._tabla(tabla, tuple("PQRSAI"), 16)
        for fila in tabla_verdad():
            self.tabla.insert("", "end", values=[int(fila[k]) for k in "PQRSAI"])
        self._actualizar_resumen()
        self.entrada.focus_set()

    @staticmethod
    def _tabla(padre, columnas, alto):
        marco = ttk.Frame(padre)
        marco.pack(fill="both", expand=True)
        tree = ttk.Treeview(marco, columns=columnas, show="headings", height=alto)
        for columna in columnas:
            tree.heading(columna, text=columna)
            tree.column(columna, width=75, minwidth=45, anchor="center")
        barra = ttk.Scrollbar(marco, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=barra.set)
        tree.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tree

    def registrar(self):
        try:
            vehiculo = Vehiculo(self.identificador.get().strip(),
                                *(v.get() for v in self.condiciones))
        except (ValueError, TypeError) as error:
            messagebox.showerror("Datos inválidos", str(error), parent=self)
            self.entrada.focus_set()
            return
        decision = evaluar(vehiculo)
        acceso = "Sí" if decision.acceso else "No"
        inspeccion = "Sí" if decision.inspeccion else "No"
        self.resultado.set(f"{vehiculo.identificador} — Acceso: {acceso} | Inspección: {inspeccion}")
        self.flota.append(vehiculo)
        self.registros.insert("", "end", values=(vehiculo.identificador,
                              *(int(v.get()) for v in self.condiciones), acceso, inspeccion))
        self.registros.yview_moveto(1)
        self._actualizar_resumen()

    def limpiar(self):
        self.identificador.set("")
        for variable in self.condiciones:
            variable.set(False)
        self.resultado.set("Ingresa un vehículo para conocer su resultado.")
        self.entrada.focus_set()

    def _actualizar_resumen(self):
        d = analizar_flota(self.flota)
        self.resumen.set(f"Total: {d['total']} | Con acceso: {d['con_acceso']} | Sin acceso: {d['sin_acceso']}\n"
                         f"Requieren inspección: {d['requieren_inspeccion']} | Acceso e inspección: {d['acceso_e_inspeccion']}")
