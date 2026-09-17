# ============================================================
# SISTEMA EXPERTO DE DIAGNÓSTICO MÉDICO Y CANALIZACIÓN (TKINTER)
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# 1. CREACIÓN DE LA VENTANA PRINCIPAL
ventana = tk.Tk()
ventana.title("Sistema Experto de Diagnóstico Médico y Triaje")
ventana.geometry("600x720")
ventana.resizable(False, False)
ventana.configure(bg="white")

# Configuración de estilos
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="white")
style.configure("TLabelframe", background="white", bordercolor="black")
style.configure("TLabelframe.Label", background="white", foreground="black")
style.configure("TLabel", background="white", foreground="black")
style.configure("TCheckbutton", background="white", foreground="black")
style.map("TCheckbutton", background=[("active", "white"), ("!active", "white")])

# Título Principal
lbl_titulo = tk.Label(
    ventana, 
    text="SISTEMA EXPERTO DE DIAGNÓSTICO MÉDICO", 
    font=("Arial", 14, "bold"), 
    bg="white", 
    fg="black", 
    pady=10
)
lbl_titulo.pack(fill=tk.X)

# Contenedor con Scroll
canvas = tk.Canvas(ventana, bg="white", highlightthickness=0)
scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
scroll_frame = tk.Frame(canvas, bg="white", bd=1, relief="solid", padx=15, pady=15)

scroll_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

form_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

def centrar_formulario(event):
    scroll_frame.update_idletasks()
    ancho_formulario = scroll_frame.winfo_reqwidth()
    x = max((event.width - ancho_formulario) // 2, 0)
    canvas.coords(form_window, x, 0)

canvas.bind("<Configure>", centrar_formulario)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 2. SECCIÓN: DATOS DEL PACIENTE
frame_paciente = ttk.LabelFrame(scroll_frame, text=" 1. Datos del Paciente ", padding=10)
frame_paciente.pack(fill=tk.X, pady=5)

ttk.Label(frame_paciente, text="Nombre completo:").grid(row=0, column=0, sticky="w", pady=2)
txt_nombre = ttk.Entry(frame_paciente, width=40)
txt_nombre.grid(row=0, column=1, pady=2)

ttk.Label(frame_paciente, text="Dirección:").grid(row=1, column=0, sticky="w", pady=2)
txt_direccion = ttk.Entry(frame_paciente, width=40)
txt_direccion.grid(row=1, column=1, pady=2)

ttk.Label(frame_paciente, text="Teléfono:").grid(row=2, column=0, sticky="w", pady=2)
txt_telefono = ttk.Entry(frame_paciente, width=40)
txt_telefono.grid(row=2, column=1, pady=2)

ttk.Label(frame_paciente, text="Edad:").grid(row=3, column=0, sticky="w", pady=2)
txt_edad = ttk.Entry(frame_paciente, width=15)
txt_edad.grid(row=3, column=1, sticky="w", pady=2)

# 3. SECCIÓN: SIGNOS VITALES
frame_vitales = ttk.LabelFrame(scroll_frame, text=" 2. Registro de Signos Vitales ", padding=10)
frame_vitales.pack(fill=tk.X, pady=5)

ttk.Label(frame_vitales, text="Frecuencia Cardíaca (BPM):").grid(row=0, column=0, sticky="w", pady=2)
txt_fc = ttk.Entry(frame_vitales, width=15)
txt_fc.grid(row=0, column=1, sticky="w", pady=2)

ttk.Label(frame_vitales, text="Oxigenación (% SpO2):").grid(row=1, column=0, sticky="w", pady=2)
txt_spo2 = ttk.Entry(frame_vitales, width=15)
txt_spo2.grid(row=1, column=1, sticky="w", pady=2)

ttk.Label(frame_vitales, text="Peso (kg):").grid(row=2, column=0, sticky="w", pady=2)
txt_peso = ttk.Entry(frame_vitales, width=15)
txt_peso.grid(row=2, column=1, sticky="w", pady=2)

ttk.Label(frame_vitales, text="Talla/Estatura (m):").grid(row=3, column=0, sticky="w", pady=2)
txt_talla = ttk.Entry(frame_vitales, width=15)
txt_talla.grid(row=3, column=1, sticky="w", pady=2)

ttk.Label(frame_vitales, text="Presión Sistólica (PAS):").grid(row=4, column=0, sticky="w", pady=2)
txt_pas = ttk.Entry(frame_vitales, width=15)
txt_pas.grid(row=4, column=1, sticky="w", pady=2)

ttk.Label(frame_vitales, text="Presión Diastólica (PAD):").grid(row=5, column=0, sticky="w", pady=2)
txt_pad = ttk.Entry(frame_vitales, width=15)
txt_pad.grid(row=5, column=1, sticky="w", pady=2)

# 4. SECCIÓN: CUESTIONARIO DE SÍNTOMAS
frame_sintomas = ttk.LabelFrame(scroll_frame, text=" 3. Evaluación de Síntomas ", padding=10)
frame_sintomas.pack(fill=tk.X, pady=5)

var_fiebre = tk.BooleanVar()
var_tos = tk.BooleanVar()
var_garganta = tk.BooleanVar()
var_dificultad_respirar = tk.BooleanVar()

for texto, variable in [
    ("¿Tiene fiebre?", var_fiebre),
    ("¿Tiene tos?", var_tos),
    ("¿Tiene dolor de garganta?", var_garganta),
    ("¿Tiene dificultad para respirar?", var_dificultad_respirar),
]:
    tk.Checkbutton(
        frame_sintomas,
        text=texto,
        variable=variable,
        bg="white",
        activebackground="white",
        selectcolor="white",
        highlightthickness=0,
    ).pack(anchor="w")

# 5. LÓGICA DEL SISTEMA EXPERTO
def evaluar_triaje_y_especialidad(P1, P2, P3, P4_sintoma, FC, SpO2, PAS, PAD):
    P5 = SpO2 < 90
    P6 = FC > 100 or FC < 50
    P7 = PAS >= 180 or PAD >= 120
    P8 = PAS > 140 or PAS < 90 or PAD > 90

    if P4_sintoma or P5 or P6 or P7 or (P1 and P2 and SpO2 < 94):
        prioridad = "ALTA"
        remision = "Urgencias Médicas"
        if P7:
            diagnostico = "Crisis hipertensiva / Riesgo cardiovascular"
        elif P5:
            diagnostico = "Insuficiencia respiratoria aguda (Hipoxia)"
        else:
            diagnostico = "Infección respiratoria severa con compromiso hemodinámico"

    elif P8 or (P1 and P2) or (P2 and P3) or P1:
        prioridad = "MEDIA"
        if P1 and P2:
            diagnostico = "Infección respiratoria aguda"
            remision = "Neumología / Medicina Interna"
        elif P2 and P3:
            diagnostico = "Irritación / Infección de vías respiratorias superiores"
            remision = "Otorrinolaringología"
        elif P8:
            diagnostico = "Alteración en la presión arterial"
            remision = "Cardiología / Medicina General"
        else:
            diagnostico = "Síndrome febril a aclarar"
            remision = "Medicina General"

    else:
        prioridad = "NORMAL"
        diagnostico = "Sin patrón patológico agudo identificado"
        remision = "Medicina General (Check-up preventivo)"

    return prioridad, diagnostico, remision

def agendar_cita(prioridad):
    ahora = datetime.now()
    if prioridad == "ALTA":
        return "INMEDIATA (Atención Prioritaria en Urgencias)", "Hoy"
    elif prioridad == "MEDIA":
        return ahora.strftime("%d/%m/%Y"), "Mismo día"
    else:
        fecha_cita = ahora + timedelta(days=3)
        return fecha_cita.strftime("%d/%m/%Y"), "Programada (Próximos días)"

def mostrar_ventana_reporte(nombre, direccion, telefono, edad, peso, talla, imc, fc, spo2, pas, pad, prioridad, diagnostico, remision, fecha_cita, tipo_cita):
    ventana_rep = tk.Toplevel(ventana)
    ventana_rep.title("Reporte Médico de Canalización")
    ventana_rep.geometry("520x550")

    txt_reporte = tk.Text(ventana_rep, font=("Consolas", 10), padx=10, pady=10)
    txt_reporte.pack(fill=tk.BOTH, expand=True)

    linea = "=" * 58
    sublinea = "-" * 58

    reporte_texto = f"""
{linea}
        REPORTE DE DIAGNÓSTICO MÉDICO Y CANALIZACIÓN
{linea}
 Fecha de Emisión : {datetime.now().strftime('%d/%m/%Y %H:%M')}
 Folio de Atención: MED-{datetime.now().strftime('%S%M%H')}
{sublinea}
 1. DATOS DEL PACIENTE
    • Nombre    : {nombre}
    • Dirección : {direccion}
    • Teléfono  : {telefono}
    • Edad      : {edad} años
    • Peso/Talla/IMC : {peso} kg / {talla} m / {imc:.1f} kg/m²

{sublinea}
 2. SIGNOS VITALES REGISTRADOS
    • Frecuencia Cardíaca : {fc} BPM
    • Oxigenación (SpO2)  : {spo2}%
    • Presión Arterial    : {pas}/{pad} mmHg

{sublinea}
 3. EVALUACIÓN Y TRIAGE
    • Diagnóstico Presuntivo : {diagnostico}
    • Nivel de Prioridad     : [{prioridad}]

{sublinea}
 4. AGENDA DE CITA Y REMISIÓN
    • Remitido a Especialidad : {remision}
    • Fecha Programada        : {fecha_cita}
    • Tipo de Asignación      : {tipo_cita}
{linea}
         PRESENTAR ESTE REPORTE EN SU UNIDAD DE SALUD
{linea}
"""
    txt_reporte.insert(tk.END, reporte_texto)
    txt_reporte.config(state=tk.DISABLED)

def procesar_evaluacion():
    try:
        nombre = txt_nombre.get().strip().title()
        direccion = txt_direccion.get().strip()
        telefono = txt_telefono.get().strip()

        if not nombre or not direccion or not telefono:
            messagebox.showwarning("Atención", "Por favor complete el nombre y la dirección.")
            return

        edad = int(txt_edad.get())
        fc = int(txt_fc.get())
        spo2 = float(txt_spo2.get())
        peso = float(txt_peso.get())
        talla = float(txt_talla.get())
        pas = int(txt_pas.get())
        pad = int(txt_pad.get())

        if any(v <= 0 for v in [edad, fc, spo2, peso, talla, pas, pad]):
            messagebox.showerror("Error de Validación", "Todos los valores numéricos deben ser mayores a 0.")
            return

    except ValueError:
        messagebox.showerror("Error de Entrada", "Asegúrese de ingresar valores numéricos válidos en la sección de signos vitales.")
        return

    imc = peso / (talla ** 2)
    P1 = var_fiebre.get()
    P2 = var_tos.get()
    P3 = var_garganta.get()
    P4_sintoma = var_dificultad_respirar.get()

    prioridad, diagnostico, remision = evaluar_triaje_y_especialidad(P1, P2, P3, P4_sintoma, fc, spo2, pas, pad)
    fecha_cita, tipo_cita = agendar_cita(prioridad)

    mostrar_ventana_reporte(
        nombre, direccion, telefono, edad, peso, talla, imc, fc, spo2, pas, pad,
        prioridad, diagnostico, remision, fecha_cita, tipo_cita
    )

# BOTÓN PROCESAR
btn_evaluar = tk.Button(
    scroll_frame, 
    text="EVALUAR PACIENTE Y GENERAR REPORTE", 
    command=procesar_evaluacion,
    bg="#0369a1", 
    fg="white", 
    font=("Arial", 10, "bold"),
    pady=8
)
btn_evaluar.pack(fill=tk.X, pady=10)

# 6. BUCLE PRINCIPAL DE LA VENTANA
ventana.mainloop()       
