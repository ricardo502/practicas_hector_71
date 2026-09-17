from datetime import datetime
import json
import os
import random
import tkinter as tk
from tkinter import messagebox, ttk

# Archivo JSON local para almacenar la base de datos de usuarios
ARCHIVO_BD = "historial_usuarios.json"


def cargar_base_datos():
    """Carga la base de datos desde un archivo JSON si existe."""
    if os.path.exists(ARCHIVO_BD):
        try:
            with open(ARCHIVO_BD, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def guardar_base_datos(bd):
    """Guarda la base de datos actualizada en el archivo JSON."""
    with open(ARCHIVO_BD, "w", encoding="utf-8") as f:
        json.dump(bd, f, indent=4, ensure_ascii=False)


def actualizar_estadisticas_usuario(nombre_usuario, equipo, diag):
    """Registra y actualiza el conteo persistente de accesos y reportes."""
    bd = cargar_base_datos()
    clave = nombre_usuario.strip().lower()
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

    if clave not in bd:
        bd[clave] = {
            "nombre_original": nombre_usuario.strip().title(),
            "total_ingresos": 1,
            "total_reportes": 1,
            "historial_equipos": [
                {
                    "fecha": fecha_actual,
                    "equipo": equipo,
                    "estado": diag["estado"],
                }
            ],
        }
        es_nuevo = True
    else:
        bd[clave]["total_ingresos"] += 1
        bd[clave]["total_reportes"] += 1
        bd[clave]["historial_equipos"].append(
            {"fecha": fecha_actual, "equipo": equipo, "estado": diag["estado"]}
        )
        es_nuevo = False

    guardar_base_datos(bd)
    return es_nuevo, bd[clave]


class SistemaDiagnosticoApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title(
            "Sistema de Diagnóstico Inteligente con Persistencia de Datos"
        )
        self.geometry("750x650")
        self.resizable(False, False)

        # Variables de control
        self.var_nombre = tk.StringVar()
        self.var_direccion = tk.StringVar()
        self.var_tipo_equipo = tk.StringVar(value="Computadora de escritorio")
        self.var_otro_equipo = tk.StringVar()

        # Variables para las preguntas (BooleanVar)
        self.var_enciende = tk.BooleanVar(value=True)
        self.var_video = tk.BooleanVar(value=True)
        self.var_especifica = tk.BooleanVar(value=True)
        self.var_lentitud = tk.BooleanVar(value=False)
        self.var_ruidos = tk.BooleanVar(value=False)

        self._crear_interfaz()

    def _crear_interfaz(self):
        # Contenedor principal con pestañas
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Pestaña 1: Diagnóstico
        self.tab_diagnostico = ttk.Frame(notebook)
        notebook.add(self.tab_diagnostico, text=" Realizar Diagnóstico ")

        # Pestaña 2: Reporte
        self.tab_reporte = ttk.Frame(notebook)
        notebook.add(self.tab_reporte, text=" Reporte Técnico ")

        self._construir_pestana_diagnostico()
        self._construir_pestana_reporte()

    def _construir_pestana_diagnostico(self):
        # Frame Datos del Cliente
        frame_cliente = ttk.LabelFrame(
            self.tab_diagnostico, text=" 1. Datos del Cliente "
        )
        frame_cliente.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_cliente, text="Nombre del Usuario:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        ttk.Entry(
            frame_cliente, textvariable=self.var_nombre, width=30
        ).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_cliente, text="Dirección / Ubicación:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        ttk.Entry(
            frame_cliente, textvariable=self.var_direccion, width=30
        ).grid(row=1, column=1, padx=5, pady=5)

        # Frame Tipo de Equipo
        frame_equipo = ttk.LabelFrame(
            self.tab_diagnostico, text=" 2. Tipo de Equipo "
        )
        frame_equipo.pack(fill="x", padx=10, pady=5)

        opciones = [
            "Computadora de escritorio",
            "Laptop",
            "All in One",
            "Servidor",
            "Otro",
        ]
        combo_equipo = ttk.Combobox(
            frame_equipo,
            textvariable=self.var_tipo_equipo,
            values=opciones,
            state="readonly",
        )
        combo_equipo.pack(side="left", padx=10, pady=5)
        combo_equipo.bind("<<ComboboxSelected>>", self._actualizar_preguntas)

        self.entry_otro = ttk.Entry(
            frame_equipo, textvariable=self.var_otro_equipo, width=25
        )
        self.entry_otro.pack(side="left", padx=5, pady=5)
        self.entry_otro.pack_forget()  # Oculto por defecto

        # Frame Preguntas de Diagnóstico
        frame_preguntas = ttk.LabelFrame(
            self.tab_diagnostico, text=" 3. Cuestionario de Evaluación "
        )
        frame_preguntas.pack(fill="both", expand=True, padx=10, pady=5)

        ttk.Checkbutton(
            frame_preguntas,
            text="1. ¿El equipo enciende correctamente?",
            variable=self.var_enciende,
        ).pack(anchor="w", padx=10, pady=3)

        ttk.Checkbutton(
            frame_preguntas,
            text="2. ¿Muestra imagen en pantalla?",
            variable=self.var_video,
        ).pack(anchor="w", padx=10, pady=3)

        self.chk_especifico = ttk.Checkbutton(
            frame_preguntas, text="", variable=self.var_especifica
        )
        self.chk_especifico.pack(anchor="w", padx=10, pady=3)

        ttk.Checkbutton(
            frame_preguntas,
            text="4. ¿Presenta lentitud o congelamientos?",
            variable=self.var_lentitud,
        ).pack(anchor="w", padx=10, pady=3)

        ttk.Checkbutton(
            frame_preguntas,
            text="5. ¿Se perciben ruidos extraños o sobrecalentamiento?",
            variable=self.var_ruidos,
        ).pack(anchor="w", padx=10, pady=3)

        # Botón de Procesar
        btn_procesar = ttk.Button(
            self.tab_diagnostico,
            text="Generar Diagnóstico",
            command=self._procesar_diagnostico,
        )
        btn_procesar.pack(pady=10)

        self._actualizar_preguntas()

    def _actualizar_preguntas(self, event=None):
        tipo = self.var_tipo_equipo.get()

        if tipo == "Otro":
            self.entry_otro.pack(side="left", padx=5, pady=5)
        else:
            self.entry_otro.pack_forget()

        if tipo == "Laptop":
            self.chk_especifico.config(
                text="3. ¿La batería retiene la carga adecuadamente?",
                state="normal",
            )
        elif tipo == "Servidor":
            self.chk_especifico.config(
                text="3. ¿El arreglo RAID / almacenamiento está saludable?",
                state="normal",
            )
        else:
            self.chk_especifico.config(
                text="3. [Pregunta específica no requerida para este equipo]",
                state="disabled",
            )

    def _construir_pestana_reporte(self):
        self.txt_reporte = tk.Text(
            self.tab_reporte, font=("Courier", 9), wrap="word"
        )
        self.txt_reporte.pack(fill="both", expand=True, padx=10, pady=10)

    def _evaluar_equipo(self, tipo_equipo):
        if not self.var_enciende.get():
            if tipo_equipo == "Laptop":
                causa = "Batería agotada/dañada o cargador defectuoso."
                recom = (
                    "Probar cargador directo sin batería o verificar centro de"
                    " carga."
                )
            elif tipo_equipo == "Servidor":
                causa = "Falla en fuente redudante o módulo PDU."
                recom = (
                    "Verificar LEDs de las fuentes traseras y líneas de"
                    " alimentación."
                )
            else:
                causa = (
                    "Cable de corriente descompuesto o fuente de poder"
                    " averiada."
                )
                recom = "Revisar cable AC, regulador de voltaje y fuente ATX."

            return {
                "estado": "CRÍTICO - Sin Encendido",
                "nivel": "ALTA",
                "causa": causa,
                "diagnostico": (
                    f"El {tipo_equipo} no realiza el arranque eléctrico."
                ),
                "recomendacion": recom,
            }

        if not self.var_video.get():
            if tipo_equipo == "Laptop":
                recom = (
                    "Probar con un monitor externo HDMI/DisplayPort para"
                    " descartar falla de flex o pantalla integrada."
                )
            else:
                recom = (
                    "Revisar cable de video (VGA/HDMI), tarjeta gráfica o"
                    " limpiar contactos de RAM."
                )

            return {
                "estado": "FALLA DE VIDEO",
                "nivel": "ALTA",
                "causa": "Problema en pantalla, memoria RAM o chip gráfico.",
                "diagnostico": (
                    f"El {tipo_equipo} enciende pero no proyecta imagen."
                ),
                "recomendacion": recom,
            }

        detalles_diag, detalles_causa, detalles_recom = [], [], []

        if tipo_equipo == "Laptop" and not self.var_especifica.get():
            detalles_diag.append("Batería con degradación severa.")
            detalles_causa.append(
                "Celdas de la batería agotadas por ciclos de vida."
            )
            detalles_recom.append("Reemplazar la batería de la laptop.")
        elif tipo_equipo == "Servidor" and not self.var_especifica.get():
            detalles_diag.append(
                "Alerta en el controlador RAID o disco degradado."
            )
            detalles_causa.append(
                "Falla física inminente en un disco del arreglo."
            )
            detalles_recom.append(
                "Reemplazar el disco afectado (Hot-Swap) y reconstruir el"
                " arreglo."
            )

        if self.var_lentitud.get():
            detalles_diag.append("Bajo rendimiento en el sistema operativo.")
            detalles_causa.append("Saturación de almacenamiento o memoria RAM.")
            detalles_recom.append(
                "Optimizar procesos de inicio y evaluar migración a SSD."
            )

        if self.var_ruidos.get():
            detalles_diag.append("Temperaturas por encima del umbral térmico.")
            detalles_causa.append("Acumulación de polvo o pasta térmica seca.")
            detalles_recom.append(
                "Realizar mantenimiento preventivo y limpieza de disipadores."
            )

        if not detalles_diag:
            return {
                "estado": "OPERATIVO",
                "nivel": "NORMAL",
                "causa": "Ninguna anomalía detectada.",
                "diagnostico": (
                    f"El {tipo_equipo} funciona dentro de los parámetros"
                    " normales."
                ),
                "recomendacion": (
                    "Realizar mantenimientos preventivos periódicos."
                ),
            }

        return {
            "estado": "ANOMALÍAS DETECTADAS",
            "nivel": "MEDIA",
            "causa": " | ".join(detalles_causa),
            "diagnostico": " | ".join(detalles_diag),
            "recomendacion": " | ".join(detalles_recom),
        }

    def _procesar_diagnostico(self):
        nombre = self.var_nombre.get().strip()
        if not nombre:
            messagebox.showwarning(
                "Dato Faltante", "Por favor ingrese el nombre del usuario."
            )
            return

        direccion = self.var_direccion.get().strip() or "No especificada"
        tipo = self.var_tipo_equipo.get()
        if tipo == "Otro":
            tipo = self.var_otro_equipo.get().strip() or "Equipo no especificado"

        num_reporte = f"REP-{random.randint(10000, 99999)}"
        ahora = datetime.now()
        fecha_str = ahora.strftime("%d/%m/%Y")
        hora_str = ahora.strftime("%H:%M")

        diag_resultado = self._evaluar_equipo(tipo)
        es_nuevo, datos_user = actualizar_estadisticas_usuario(
            nombre, tipo, diag_resultado
        )

        # Generar texto del reporte
        linea = "=" * 68
        sublinea = "-" * 68
        reporte_txt = f"""
{linea}
                REPORTE TÉCNICO Y ESTADÍSTICO DE SERVICIO         
{linea}
 Folio del Reporte : {num_reporte:<20} Fecha: {fecha_str}
 Estatus Ticket    : REGISTRADO           Hora : {hora_str}
{sublinea}
 1. DATOS DEL CLIENTE
    • Nombre Registrado : {datos_user['nombre_original']}
    • Dirección         : {direccion}

{sublinea}
 2. REPORTES Y ESTADÍSTICAS DEL USUARIO
"""
        if es_nuevo:
            reporte_txt += (
                "    • Tipo de Usuario    : [NUEVO REGISTRO]\n    • Primer"
                " ingreso detectado en la base de datos.\n"
            )
        else:
            reporte_txt += f"""    • Tipo de Usuario    : [USUARIO RECURRENTE]
    • Total de ingresos al sistema   : {datos_user['total_ingresos']} veces
    • Equipos evaluados acumulados  : {datos_user['total_reportes']} reportes
"""

        reporte_txt += f"""
{sublinea}
 3. DIAGNÓSTICO ESPECÍFICO DEL EQUIPO
    • Tipo de Equipo     : {tipo}
    • Diagnóstico        : {diag_resultado['diagnostico']}
    • Nivel de Prioridad : [{diag_resultado['nivel']}]
    • Posible Causa      : {diag_resultado['causa']}

{sublinea}
 4. PLAN DE ACCIÓN Y RECOMENDACIÓN
    • Acción Sugerida    : {diag_resultado['recomendacion']}

{sublinea}
 5. HISTORIAL RECIENTE DE EQUIPOS EVALUADOS POR ESTE USUARIO
"""
        for idx, item in enumerate(datos_user["historial_equipos"], 1):
            reporte_txt += f"    {idx}. [{item['fecha']}] - {item['equipo']} -> Estado: {item['estado']}\n"

        reporte_txt += f"\n{linea}\n                   FIN DEL INFORME TÉCNICO                        \n{linea}\n"

        # Mostrar en la pestaña de Reporte
        self.txt_reporte.delete("1.0", tk.END)
        self.txt_reporte.insert(tk.END, reporte_txt)

        messagebox.showinfo(
            "Éxito",
            "Diagnóstico procesado y registrado correctamente en la base de"
            " datos.",
        )


if __name__ == "__main__":
    app = SistemaDiagnosticoApp()
    app.mainloop()     