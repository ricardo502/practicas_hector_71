import time
import random
from datetime import datetime


def crima():
    temperatura = round(random.uniform(15, 35), 1)
    humedad = round(random.uniform(40, 90), 1)
    return temperatura, humedad


def elegir_accion(temperatura, humedad):
    if temperatura < 18:
        return "Prender calefacción"
    if temperatura > 30:
        if humedad > 70:
            return "Prender aire acondicionado para deshumidificar"
        return "Prender ventilador"
    return "Dejar equipos apagados"


def registrar(temperatura, humedad, accion):
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje = f"{hora} | {temperatura} °C | Humedad: {humedad}% | {accion}"
    print(mensaje)
    with open("historial_clima.txt", "a", encoding="utf-8") as archivo:
        archivo.write(mensaje + "\n")


def iniciar():
    print("Monitor de clima. Presiona Ctrl + C para salir.")
    print("Las lecturas se guardan en historial_clima.txt")
    try:
        while True:
            temperatura, humedad = crima()
            accion = elegir_accion(temperatura, humedad)
            registrar(temperatura, humedad, accion)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nMonitor finalizado.")


if __name__ == "__main__":
    iniciar()
