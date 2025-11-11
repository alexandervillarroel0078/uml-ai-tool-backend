# app/routers/ia_edicion.py
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.uml import Diagram
from app.models.user import User
from app.routers.auth import get_current_user
from app.services.ia_editor_text import procesar_edicion_ia
from app.services.ia_edicion_bd import aplicar_edicion_a_bd
import logging

router = APIRouter(prefix="/ia", tags=["IA Edición"])
log = logging.getLogger("app.routers.ia_edicion")

@router.post("/editar_diagrama")
def editar_diagrama(
    body: dict = Body(...),  # 👈 se requiere JSON
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user)
):
    diagram_id = body.get("diagram_id")
    prompt = body.get("prompt")

    if not diagram_id or not prompt:
        raise HTTPException(status_code=400, detail="Faltan campos: diagram_id y prompt son requeridos")

    diagram = db.query(Diagram).filter(Diagram.id == diagram_id).first()
    if not diagram:
        raise HTTPException(status_code=404, detail="Diagrama no encontrado")

    # 1️⃣ Construir JSON del diagrama actual
    diagram_data = {
        "diagram": {
            "id": str(diagram.id),
            "title": diagram.title,
            "classes": [
                {
                    "name": c.nombre,
                    "attributes": [
                        {
                            "name": a.nombre,
                            "type": a.tipo,
                            "requerido": a.requerido,
                            "es_primaria": a.es_primaria,
                        }
                        for a in c.atributos
                    ],
                }
                for c in diagram.classes
            ],
            "relations": [
                {
                    "from": r.origen.nombre,
                    "to": r.destino.nombre,
                    "type": r.tipo.value,
                }
                for r in diagram.relations
            ],
        }
    }

    # 2️⃣ IA genera nuevo JSON
    try:
        nuevo_json = procesar_edicion_ia(diagram_data, prompt)
    except Exception as e:
        log.error(f"Error IA: {e}")
        raise HTTPException(status_code=500, detail=f"Error IA: {e}")

    # 3️⃣ Aplicar cambios directamente al mismo diagrama
    try:
        aplicar_edicion_a_bd(nuevo_json, db, diagram_id)
    except Exception as e:
        log.error(f"Error aplicando edición a BD: {e}")
        raise HTTPException(status_code=500, detail=f"Error BD: {e}")

    log.info(f"✅ Edición IA aplicada correctamente al diagrama {diagram.title}")
    return {
        "ok": True,
        "msg": "✅ Diagrama actualizado por IA",
        "nuevo_diagrama": nuevo_json
    }
