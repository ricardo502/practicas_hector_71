# LogiSmart Python Suite

Aplicación con interfaz gráfica Tkinter en Python para evaluar vehículos, generar la tabla de
verdad y analizar una flota. Solo usa la biblioteca estándar; requiere Python 3.10+.

## Alcance y supuestos

El material proporcionado incluye la descripción general y una fotografía del
pizarrón, pero no las preguntas de las cuatro secciones del examen. Este proyecto
implementa lo disponible; no pretende reconstruir las preguntas faltantes.

La fotografía se interpreta así (la definición de S es poco legible y se asume
que significa certificación vigente):

| Variable | Significado |
| --- | --- |
| P | Vehículo con autorización |
| Q | El peso excede el límite |
| R | Carga de material peligroso |
| S | Conductor con certificación vigente |
| A | Acceso: `P and S and not Q` |
| I | Inspección: `P and (R or Q)` |

Acceso e inspección son resultados independientes. Un vehículo autorizado, sin
sobrepeso, con carga peligrosa y certificación vigente obtiene ambos resultados
verdaderos. No se añadió una prioridad entre ellos, pues no aparece en el material.
Sin autorización, ambos son falsos según estas fórmulas.
El sobrepeso se recibe como booleano porque no se proporcionó un límite numérico.
Los conteos de acceso e inspección pueden superponerse.

## Ejecución

Desde la carpeta del repositorio:

```powershell
cd LogiSmart
python main.py
python -m unittest discover -s tests -v
```

`python main.py` abre la ventana. Escribe el identificador, marca las condiciones
que se cumplen y pulsa **Evaluar y registrar**. La ventana muestra los resultados,
los registros y el resumen de flota. Cada evaluación cuenta como un registro.
**Limpiar formulario** prepara otra entrada sin borrar los registros.
Los datos se guardan en memoria hasta cerrar la ventana.
La pestaña **Tabla de verdad** muestra las 16 combinaciones.
Tkinter viene incluido con la instalación habitual de Python para Windows.

## Organización

- `vehiculo.py`: modelo inmutable y validación de entradas.
- `decision.py`: lógica de acceso e inspección.
- `analisis.py`: tabla de verdad y conteos de flota, incluida una flota vacía.
- `main.py`: inicio de la aplicación de escritorio.
- `interfaz.py`: formulario, registros, resumen y tabla con Tkinter.
- `tests/test_logismart.py`: pruebas de las 16 combinaciones, análisis y entradas inválidas.

Para las 16 combinaciones se esperan 2 accesos, 6 inspecciones y 1 caso con ambos.
No se requiere instalar dependencias externas.
