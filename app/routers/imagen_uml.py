# app/routers/imagen_uml.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db

from app.services.servicio_archivos import guardar_imagen
from app.services.servicio_analisis import analizar_imagen_uml
from app.services.servicio_importacion import importar_json_a_bd

from app.routers.auth import get_current_user  # ✅ importa tu función de autenticación
from app.models.user import User

router = APIRouter()

@router.post("/subir_imagen")
async def subir_imagen(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    usuario_actual: User = Depends(get_current_user)  # ✅ usuario logueado
):
    """
    📤 Sube una imagen UML, la analiza automáticamente con IA,
    guarda el JSON y lo inserta directamente en la base de datos.
    """
    try:
        # 1️⃣ Guardar imagen
        ruta_imagen = guardar_imagen(file)

        # 2️⃣ Analizar con IA (devuelve JSON)
        uml_json = analizar_imagen_uml(ruta_imagen)

        # 3️⃣ Insertar en BD con el owner_id correcto
        importar_json_a_bd(uml_json, db, owner_id=usuario_actual.id)

        return {
            "ok": True,
            "msg": f"✅ Diagrama procesado e insertado correctamente para {usuario_actual.name}.",
            "uml": uml_json
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
