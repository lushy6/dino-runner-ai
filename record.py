import json
from constants import ARCHIVO_RECORD


def cargar_record():
    try:
        with open(ARCHIVO_RECORD, "r", encoding="utf-8") as f:
            return int(json.load(f).get("record", 0))
    except Exception:
        return 0


def guardar_record(valor):
    try:
        with open(ARCHIVO_RECORD, "w", encoding="utf-8") as f:
            json.dump({"record": int(valor)}, f)
    except Exception:
        pass


