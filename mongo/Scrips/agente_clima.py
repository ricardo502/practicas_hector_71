import random
import sys
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tkinter import messagebox
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config.conexion import conectar


def crima():
    temperatura = round(random.uniform(15, 35), 1)
    humedad = round(random.uniform(40, 90), 1)
    return temperatura, humedad


def accion_1(temperatura, humedad):
    if temperatura < 18:
        return "Prender calefacción"
    if temperatura > 30:
        if humedad > 70:
            return "Prender aire acondicionado para deshumidificar"
        return "Prender ventilador"
    return "Dejar equipos apagados"


def registrar(temperatura, humedad, accion, coleccion):
    resultado = coleccion.insert_one({
        "fecha": datetime.now(timezone.utc),
        "temperatura": temperatura,
        "humedad": humedad,
        "accion": accion,
    })
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje = f"{hora} | {temperatura} °C | Humedad: {humedad}% | {accion}"
    print(mensaje)
    with open("historial_clima.txt", "a", encoding="utf-8") as archivo:
        archivo.write(mensaje + "\n")
    return resultado.inserted_id


def iniciar():
    ventana = tk.Tk()
    ventana.title("Agente de climatización")
    ventana.geometry("460x330")

    temperatura_texto = tk.StringVar(value="Temperatura: °C")
    humedad_texto = tk.StringVar(value="Humedad: %")
    accion_texto = tk.StringVar(value="Acción: sin lectura")
    estado = tk.StringVar(value="Simulación detenida")
    tarea = None
    ejecutor = ThreadPoolExecutor(max_workers=1)
    cliente = None
    coleccion = None
    envio = None

    def enviar(temperatura, humedad, accion):
        nonlocal cliente, coleccion
        if cliente is None:
            cliente, coleccion = conectar()
        return registrar(temperatura, humedad, accion, coleccion)

    def comprobar_envio():
        nonlocal tarea, envio
        if not envio.done():
            tarea = ventana.after(100, comprobar_envio)
            return
        tarea = None
        try:
            envio.result()
        except Exception as error:
            detener()
            messagebox.showerror("Error al guardar", str(error), parent=ventana)
            return
        finally:
            envio = None
        estado.set("Guardado en Atlas: " + datetime.now().strftime("%H:%M:%S"))
        tarea = ventana.after(3000, actualizar)

    def actualizar():
        nonlocal tarea, envio
        tarea = None
        temperatura, humedad = crima()
        accion = accion_1(temperatura, humedad)
        temperatura_texto.set(f"Temperatura: {temperatura} °C")
        humedad_texto.set(f"Humedad: {humedad}%")
        accion_texto.set(f"Acción: {accion}")
        estado.set("Enviando lectura a Atlas...")
        envio = ejecutor.submit(enviar, temperatura, humedad, accion)
        tarea = ventana.after(100, comprobar_envio)

    def comenzar():
        boton_iniciar.config(state="disabled")
        boton_detener.config(state="normal")
        if envio is not None:
            comprobar_envio()
        else:
            actualizar()

    def detener():
        nonlocal tarea
        if tarea is not None:
            ventana.after_cancel(tarea)
            tarea = None
        boton_iniciar.config(state="normal")
        boton_detener.config(state="disabled")
        estado.set("Simulación detenida")

    def cerrar():
        detener()
        def cerrar_conexion():
            if cliente is not None:
                cliente.close()
        ejecutor.submit(cerrar_conexion)
        ejecutor.shutdown(wait=False)
        ventana.destroy()

    tk.Label(ventana, text="Climatización simulada", font=("Arial", 16)).pack(pady=12)
    tk.Label(ventana, textvariable=temperatura_texto, font=("Arial", 12)).pack(pady=5)
    tk.Label(ventana, textvariable=humedad_texto, font=("Arial", 12)).pack(pady=5)
    tk.Label(ventana, textvariable=accion_texto, wraplength=420).pack(pady=10)

    botones = tk.Frame(ventana)
    botones.pack(pady=10)
    boton_iniciar = tk.Button(botones, text="Iniciar", width=12, command=comenzar)
    boton_iniciar.pack(side="left", padx=5)
    boton_detener = tk.Button(
        botones, text="Detener", width=12, command=detener, state="disabled"
    )
    boton_detener.pack(side="left", padx=5)

    tk.Label(ventana, textvariable=estado).pack(pady=5)
    ventana.protocol("WM_DELETE_WINDOW", cerrar)
    ventana.mainloop()


if __name__ == "__main__":
    iniciar()



