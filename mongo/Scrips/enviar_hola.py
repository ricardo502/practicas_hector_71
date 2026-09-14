import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config.conexion import conectar
from pymongo.errors import PyMongoError


def main():
    try:
        cliente, coleccion = conectar()
        with cliente:
            resultado = coleccion.insert_one({"mensaje": "hola buenas tardes"})
            print(f"Mensaje insertado en {coleccion.full_name}")
            print(f"ID: {resultado.inserted_id}")
            documento = coleccion.find_one({"_id": resultado.inserted_id})
            if documento is None:
                raise RuntimeError("No se pudo verificar el documento insertado")
            print(f"Mensaje verificado: {documento['mensaje']}")
    except (PyMongoError, ValueError, RuntimeError) as error:
        print(f"Error de MongoDB: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
