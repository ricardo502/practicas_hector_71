
import tkinter as tk
import tkinter.messagebox as messagebox    
import tkinter.simpledialog as simpledialog
import tkinter.ttk as ttk
import random
import time 

ventana = tk.Tk()
ventana.geometry("400x300")
ventana.pack_propagate(False)

ventana.title("LogISmart")
    


class vehiculos:
    def __init__(self, nombre, tipo, velocidad):
        if not isinstance(nombre, str):
            raise ValueError("El nombre debe ser una cadena de texto.")
        if not isinstance(tipo, str):
            raise ValueError("El tipo debe ser una cadena de texto.")
        if not isinstance(velocidad, (int, float)):
            raise ValueError("La velocidad debe ser un número.")
        self.nombre = nombre
        self.tipo = tipo
        self.velocidad = velocidad