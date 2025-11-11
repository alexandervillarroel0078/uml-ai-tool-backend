# app/services/servicio_archivos.py
import os
from fastapi import UploadFile

CARPETA_SUBIDAS = "app/uploads"

def guardar_imagen(file: UploadFile) -> str:
    if not os.path.exists(CARPETA_SUBIDAS):
        os.makedirs(CARPETA_SUBIDAS)

    ruta_destino = os.path.join(CARPETA_SUBIDAS, file.filename)
    with open(ruta_destino, "wb") as buffer:
        buffer.write(file.file.read())

    return ruta_destino
