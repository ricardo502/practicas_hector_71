"""Agente de climatización con sensores simulados y registro en TXT."""

import time
import random
from datetime import datetime


class AgenteClimatizacion:
    def __init__(self, archivo_log="registro_agente.txt"):
        self.temperatura = 0.0
        self.humedad = 0.0
        self.accion = ""
        self.archivo_log = archivo_log

    def percibir_simulado(self):
        """Simula lecturas del entorno con valores aleatorios razonables."""
        self.temperatura = round(random.uniform(15.0, 35.0), 1)
        self.humedad = round(random.uniform(40.0, 90.0), 1)

    def tomar_decision(self):
        """Aplica la regla condición-acción basada en la percepción."""
        if self.temperatura > 30 and self.humedad > 70:
            self.accion = "Encender aire acondicionado (Modo Deshumidificador)"
        elif self.temperatura > 30:
            self.accion = "Encender ventilador"
        elif self.temperatura < 18:
            self.accion = "Encender calefacción"
        else:
            self.accion = "Mantener sistema apagado"

    def guardar_registro(self):
        """Guarda la percepción y decisión en un archivo de texto con timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea_log = (
            f"[{timestamp}] Temp: {self.temperatura}°C | "
            f"Humedad: {self.humedad}% | Acción: {self.accion}\n"
        )
        with open(self.archivo_log, "a", encoding="utf-8") as f:
            f.write(linea_log)

    def mostrar_resultado(self):
        """Muestra el estado actual en la consola."""
        print(f"Percepción -> Temp: {self.temperatura}°C | Humedad: {self.humedad}%")
        print(f"Acción -> {self.accion}")
        print("Registrado en archivo log.\n" + "-" * 50)

    def ejecutar_bucle(self, intervalo_segundos=3):
        """Ejecuta el ciclo continuo del agente."""
        print(f"--- INICIANDO AGENTE EN BUCLE (Intervalo: {intervalo_segundos}s) ---")
        print(f"Guardando datos en: '{self.archivo_log}'")
        print("Presiona Ctrl + C para detener la simulación.\n")
        try:
            while True:
                self.percibir_simulado()
                self.tomar_decision()
                self.guardar_registro()
                self.mostrar_resultado()
                time.sleep(intervalo_segundos)
        except KeyboardInterrupt:
            print("\nSimulación detenida por el usuario.")


# --- EJECUCIÓN DEL AGENTE ---
if __name__ == "__main__":
    agente = AgenteClimatizacion()
    agente.ejecutar_bucle(intervalo_segundos=3)

# Simulación con random.uniform: Genera valores aleatorios continuos para la
# temperatura (15 °C a 35 °C) y humedad (40% a 90%).
# Bucle while True: Corre indefinidamente hasta que presiones Ctrl + C en la consola.
# Manejo del Log (with open): Abre el archivo en modo append ("a"),
# lo que significa que añadirá nuevas filas al final sin borrar las anteriores.
# Marcas de tiempo (datetime): Utiliza el módulo de fecha y hora para identificar
# cuándo ocurrió cada lectura en el archivo .txt.
