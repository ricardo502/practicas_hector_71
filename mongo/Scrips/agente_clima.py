import random
import math
import sys
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tkinter import messagebox, ttk
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


def datos_lectura(temperatura, humedad):
    try:
        temperatura = float(temperatura)
        humedad = float(humedad)
    except ValueError:
        raise ValueError("Escribe números válidos en temperatura y humedad.") from None
    if not math.isfinite(temperatura) or not math.isfinite(humedad):
        raise ValueError("Los valores deben ser números finitos.")
    if not 0 <= humedad <= 100:
        raise ValueError("La humedad debe estar entre 0 y 100%.")
    return {"temperatura": temperatura, "humedad": humedad,
            "accion": accion_1(temperatura, humedad)}


def iniciar():
    ventana = tk.Tk()
    ventana.title("Agente de climatización")
    ventana.geometry("850x650")

    temperatura_texto = tk.StringVar(value="Temperatura: °C")
    humedad_texto = tk.StringVar(value="Humedad: %")
    accion_texto = tk.StringVar(value="Acción: sin lectura")
    estado = tk.StringVar(value="Simulación detenida")
    tarea = None
    ejecutor = ThreadPoolExecutor(max_workers=1)
    cliente = None
    coleccion = None
    envio = None

    def obtener_coleccion():
        nonlocal cliente, coleccion
        if cliente is None:
            cliente, coleccion = conectar()
        return coleccion

    def enviar(temperatura, humedad, accion):
        return registrar(temperatura, humedad, accion, obtener_coleccion())

    # Comparte el ejecutor con la simulación: MongoDB nunca bloquea la ventana.
    documentos = {}
    consulta_tarea = None
    crud_ocupado = False

    def ejecutar_crud(operacion):
        nonlocal crud_ocupado, consulta_tarea
        if crud_ocupado:
            return
        crud_ocupado = True
        for boton in botones_crud:
            boton.config(state="disabled")
        estado_crud.set("Consultando Atlas...")

        def trabajo():
            col = obtener_coleccion()
            operacion(col)
            return list(col.find({"temperatura": {"$exists": True},
                                  "humedad": {"$exists": True}})
                        .sort("fecha", -1).limit(100))

        futuro = ejecutor.submit(trabajo)

        def comprobar():
            nonlocal crud_ocupado, consulta_tarea
            if not futuro.done():
                consulta_tarea = ventana.after(100, comprobar)
                return
            consulta_tarea = None
            try:
                lecturas = futuro.result()
                for fila in tabla.get_children():
                    tabla.delete(fila)
                documentos.clear()
                for doc in lecturas:
                    clave = str(doc["_id"])
                    documentos[clave] = doc
                    fecha = doc.get("fecha")
                    if isinstance(fecha, datetime):
                        if fecha.tzinfo is None:
                            fecha = fecha.replace(tzinfo=timezone.utc)
                        fecha = fecha.astimezone().strftime("%Y-%m-%d %H:%M:%S")
                    tabla.insert("", "end", iid=clave, values=(
                        fecha or "", doc["temperatura"], doc["humedad"],
                        doc.get("accion", "")))
                estado_crud.set(f"{len(lecturas)} lecturas (máximo 100 recientes).")
            except Exception as error:
                estado_crud.set("No se pudo completar la operación o actualizar la lista.")
                messagebox.showerror("Error de MongoDB", str(error), parent=ventana)
            finally:
                crud_ocupado = False
                for boton in botones_crud:
                    boton.config(state="normal")

        consulta_tarea = ventana.after(100, comprobar)

    def seleccionar(event=None):
        seleccion = tabla.selection()
        if seleccion:
            doc = documentos[seleccion[0]]
            temperatura_manual.set(str(doc["temperatura"]))
            humedad_manual.set(str(doc["humedad"]))

    def actualizar_lectura():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona una lectura", "Selecciona una fila para editarla.", parent=ventana)
            return
        try:
            datos = datos_lectura(temperatura_manual.get(), humedad_manual.get())
        except ValueError as error:
            messagebox.showerror("Datos inválidos", str(error), parent=ventana)
            return
        identificador = documentos[seleccion[0]]["_id"]
        def operacion(col):
            resultado = col.update_one({"_id": identificador}, {"$set": datos})
            if resultado.matched_count == 0:
                raise ValueError("La lectura ya no existe. Actualiza la lista.")
        ejecutar_crud(operacion)

    def eliminar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona una lectura", "Selecciona una fila para eliminarla.", parent=ventana)
            return
        identificador = documentos[seleccion[0]]["_id"]
        if messagebox.askyesno("Eliminar lectura", "¿Eliminar la lectura seleccionada de Atlas?", parent=ventana):
            def operacion(col):
                resultado = col.delete_one({"_id": identificador})
                if resultado.deleted_count == 0:
                    raise ValueError("La lectura ya no existe. Actualiza la lista.")
            ejecutar_crud(operacion)

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
        if consulta_tarea is not None:
            ventana.after_cancel(consulta_tarea)
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

    panel = ttk.LabelFrame(ventana, text="Lecturas de Atlas")
    panel.pack(fill="both", expand=True, padx=12, pady=8)
    formulario = ttk.Frame(panel)
    formulario.pack(fill="x", padx=8, pady=8)
    temperatura_manual = tk.StringVar()
    humedad_manual = tk.StringVar()
    ttk.Label(formulario, text="Temperatura (°C):").pack(side="left")
    ttk.Entry(formulario, textvariable=temperatura_manual, width=12).pack(side="left", padx=8)
    ttk.Label(formulario, text="Humedad (%):").pack(side="left")
    ttk.Entry(formulario, textvariable=humedad_manual, width=12).pack(side="left", padx=8)
    barra = ttk.Frame(panel)
    barra.pack(fill="x", padx=8)
    botones_crud = []
    for texto, comando in (
        ("Consultar / refrescar", lambda: ejecutar_crud(lambda col: None)),
        ("Actualizar", actualizar_lectura),
        ("Eliminar", eliminar),
    ):
        boton = ttk.Button(barra, text=texto, command=comando)
        boton.pack(side="left", padx=4)
        botones_crud.append(boton)
    ttk.Label(panel, text="Selecciona una fila para editar. La acción se calcula automáticamente.").pack(pady=5)
    listado = ttk.Frame(panel)
    listado.pack(fill="both", expand=True, padx=8)
    tabla = ttk.Treeview(listado, columns=("fecha", "temperatura", "humedad", "accion"), show="headings", selectmode="browse")
    for nombre, titulo, ancho in (("fecha", "Fecha local", 160), ("temperatura", "Temperatura °C", 110),
                                  ("humedad", "Humedad %", 100), ("accion", "Acción", 330)):
        tabla.heading(nombre, text=titulo)
        tabla.column(nombre, width=ancho)
    scroll = ttk.Scrollbar(listado, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")
    tabla.pack(side="left", fill="both", expand=True)
    tabla.bind("<<TreeviewSelect>>", seleccionar)
    estado_crud = tk.StringVar(value="Pulsa Consultar para cargar las lecturas.")
    ttk.Label(panel, textvariable=estado_crud).pack(pady=5)
    ventana.protocol("WM_DELETE_WINDOW", cerrar)
    ventana.mainloop()


if __name__ == "__main__":
    iniciar()

