from pathlib import Path

from dotenv import dotenv_values
from pymongo import MongoClient


def conectar():
    """Lee el .env del proyecto y devuelve el cliente y la coleccion."""
    ruta = Path(__file__).resolve().parents[1] / ".env"
    config = dotenv_values(ruta, encoding="utf-8-sig")
    claves = ("MONGO_USER", "MONGO_PASSWORD", "MONGO_CLUSTER", "MONGO_DB", "MONGO_COLLECTION")
    for clave in claves:
        if not config.get(clave) or "REEMPLAZA" in config[clave]:
            raise ValueError(f"Completa {clave} en el archivo .env")

    cliente = MongoClient(
        f"mongodb+srv://{config['MONGO_CLUSTER']}/?retryWrites=true&w=majority",
        username=config["MONGO_USER"],
        password=config["MONGO_PASSWORD"],
        authSource="admin",
        serverSelectionTimeoutMS=15000,
        connectTimeoutMS=15000,
    )
    try:
        cliente.admin.command("ping")
    except Exception:
        cliente.close()
        raise
    return cliente, cliente[config["MONGO_DB"]][config["MONGO_COLLECTION"]]
