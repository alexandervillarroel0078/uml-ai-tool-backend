# app/routers/diagramas.py
# POST
# http://localhost:8000/diagrams
# {
#   "title": "Mi primer diagrama"
# } 
# GET
# http://localhost:8000/diagrams?page=1&limit=20
from uuid import UUID
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.encoders import jsonable_encoder
from app.db import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.uml import Clase, Relacion
from app.models.uml import Diagram
from app.models.collaborator import DiagramCollaborator
from app.schemas.diagram import DiagramCreate, DiagramOut, DiagramList
from app.schemas.clase_completa import ClaseCompletaOut, ClaseCompletaOutLight,RelacionOutExpanded
from app.models.collaborator import DiagramCollaborator
from ._helpers import get_my_diagram
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/diagrams", tags=["diagrams"])
log = logging.getLogger("app.routers.diagramas")


@router.post("", response_model=DiagramOut, status_code=status.HTTP_201_CREATED)
def create_diagram(
    body: DiagramCreate,
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user),
):
    log.info(f"➕ Crear diagrama -> user_id={me.id}, title={body.title}")
    d = Diagram(title=body.title, owner_id=me.id)
    db.add(d); db.commit(); db.refresh(d)
    log.debug(f"✅ Diagrama creado -> id={d.id}, title={d.title}")
    return d

# 🔹 Listar diagramas donde soy colaborador (no dueño)
# 🔹 Listar diagramas donde soy colaborador (no dueño)
@router.get("/shared", response_model=List[DiagramOut])
def list_shared_diagrams(
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user),
):
    log.info(f"👥 Listar diagramas compartidos -> user_id={me.id}")

    diagrams = (
        db.query(Diagram)
        .join(DiagramCollaborator)
        .filter(DiagramCollaborator.user_id == me.id)
        .order_by(Diagram.updated_at.desc())
        .all()
    )

    if not diagrams:
        log.debug(f"⚠️ No hay diagramas compartidos -> user_id={me.id}")
    else:
        log.debug(f"✅ {len(diagrams)} diagramas compartidos encontrados -> user_id={me.id}")

    return diagrams

@router.get("", response_model=DiagramList)
def list_diagrams(
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user),
):
    if page < 1:
        page = 1
    if limit < 1:
        limit = 20

    log.info(f"📥 Listar diagramas (propios + compartidos) -> user_id={me.id}")

    q_own = db.query(Diagram).filter(Diagram.owner_id == me.id)
    q_shared = (
        db.query(Diagram)
        .join(DiagramCollaborator)
        .filter(DiagramCollaborator.user_id == me.id)
    )

    diagrams = q_own.union_all(q_shared).all()
    diagrams = sorted(diagrams, key=lambda d: d.updated_at, reverse=True)
    total = len(diagrams)

    items_out = []
    for d in diagrams:
        collaborators_out = [
            {
                "user_id": c.user_id,
                "diagram_id": str(c.diagram_id),
                "added_at": c.added_at,
            }
            for c in getattr(d, "collaborators", [])
        ]

        items_out.append({
            "id": str(d.id),
            "title": d.title,
            "owner_id": d.owner_id,
            "updated_at": d.updated_at,
            "collaborators": collaborators_out,
            "is_owner": (d.owner_id == me.id)  # 👈 Marca si es tuyo o compartido
        })

    return DiagramList.model_validate({
        "items": items_out,
        "page": page,
        "limit": limit,
        "total": total
    })

# @router.get("/{diagram_id}", response_model=DiagramOut)
# def get_diagram(
#     diagram_id: UUID,
#     db: Session = Depends(get_db),
#     me: User = Depends(get_current_user),
# ):
#     log.info(f"🔍 Obtener diagrama -> user_id={me.id}, diagram_id={diagram_id}")
#     d = db.query(Diagram).filter(Diagram.id == diagram_id, Diagram.owner_id == me.id).one_or_none()
#     if not d:
#         log.warning(f"⚠️ Diagrama no encontrado -> diagram_id={diagram_id}, user_id={me.id}")
#         raise HTTPException(404, "Diagrama no encontrado")
#     log.debug(f"✅ Diagrama encontrado -> id={d.id}, title={d.title}")
#     return d

@router.get("/{diagram_id}", response_model=dict)
def get_diagram(
    diagram_id: UUID,
    db: Session = Depends(get_db),
    me: "User" = Depends(get_current_user),
):
    log.info(f"🔍 Obtener diagrama -> user_id={me.id}, diagram_id={diagram_id}")

    # Buscar diagrama
    d = db.query(Diagram).filter(Diagram.id == diagram_id).first()
    if not d:
        raise HTTPException(404, "Diagrama no encontrado")

    # Verificar acceso
    es_colaborador = db.query(DiagramCollaborator).filter(
        DiagramCollaborator.diagram_id == diagram_id,
        DiagramCollaborator.user_id == me.id,
    ).first()
    if d.owner_id != me.id and not es_colaborador:
        raise HTTPException(403, "No tienes permiso para acceder a este diagrama")

    # === Cargar clases ===
    clases = db.query(Clase).filter(Clase.diagram_id == d.id).all()
    clases_out = []
    for c in clases:
        db.refresh(c)
        parsed = ClaseCompletaOut.model_validate(c).model_dump(by_alias=False)
        log.info(f"🧩 Clase -> {parsed.get('name')} | atributos={len(parsed.get('atributos', []))}")
        for att in parsed.get("atributos", []):
            log.info(f"   🔹 Atributo -> {att}")
        clases_out.append(parsed)

    # === Cargar relaciones ===
    relaciones = db.query(Relacion).filter(Relacion.diagram_id == d.id).all()
    relaciones_out = []
    for r in relaciones:
        rel = RelacionOutExpanded.model_validate({
            **r.__dict__,
            "origen": ClaseCompletaOutLight.model_validate(r.origen),
            "destino": ClaseCompletaOutLight.model_validate(r.destino),
        }).model_dump(by_alias=True)
        log.info(f"🔗 Relación -> {rel}")
        relaciones_out.append(rel)


    result = {
        "id": str(d.id),
        "title": d.title,
        "owner_id": d.owner_id,
        "updated_at": d.updated_at,
        "collaborators": [
            {
                "user_id": c.user_id,
                "diagram_id": str(c.diagram_id),
                "added_at": c.added_at,
            }
            for c in getattr(d, "collaborators", [])
        ],
        "is_owner": (d.owner_id == me.id),
        "clases": clases_out,
        "relaciones": relaciones_out,
    }

    log.info(f"✅ Respuesta final -> {result}")
    return JSONResponse(content=jsonable_encoder(result))



@router.delete("/{diagram_id}", status_code=204)
def delete_diagram(
    diagram_id: UUID,
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user),
):
    log.info(f"🗑️ Eliminar diagrama -> user_id={me.id}, diagram_id={diagram_id}")
    d = db.query(Diagram).filter(Diagram.id == diagram_id, Diagram.owner_id == me.id).one_or_none()
    if not d:
        log.warning(f"⚠️ Intento de eliminar diagrama inexistente -> diagram_id={diagram_id}, user_id={me.id}")
        raise HTTPException(404, "Diagrama no encontrado")

    db.delete(d); db.commit()
    log.debug(f"✅ Diagrama eliminado -> id={diagram_id}, user_id={me.id}")
    return


# @router.get("/{diagram_id}/full", response_model=dict)
# def get_diagram_full(
#     diagram_id: UUID,
#     db: Session = Depends(get_db),
#     me: User = Depends(get_current_user),
# ):
#     d = get_my_diagram(db, me, diagram_id)

#     # Todas las clases con atributos y métodos
#     clases = db.query(Clase).filter(Clase.diagram_id == d.id).all()
#     clases_out = [ClaseCompletaOut.model_validate(c) for c in clases]

#     # Todas las relaciones expandidas
#     relaciones = db.query(Relacion).filter(Relacion.diagram_id == d.id).all()
#     relaciones_out = []
#     for r in relaciones:
#         relaciones_out.append(
#             RelacionOutExpanded.model_validate({
#                 **r.__dict__,
#                 "origen": ClaseCompletaOutLight.model_validate(r.origen),
#                 "destino": ClaseCompletaOutLight.model_validate(r.destino),
#             })
#         )

#     return {
#         "id": str(d.id),
#         "title": d.title,
#         "clases": clases_out,
#         "relaciones": relaciones_out
#     }
@router.get("/{diagram_id}/full", response_model=dict)
def get_diagram_full(
    diagram_id: UUID,
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user),
):
    # 🔹 Buscar el diagrama
    d = db.query(Diagram).filter(Diagram.id == diagram_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Diagrama no encontrado")

    # 🔹 Verificar si el usuario es el propietario o colaborador
    es_colaborador = (
        db.query(DiagramCollaborator)
        .filter(DiagramCollaborator.diagram_id == diagram_id, DiagramCollaborator.user_id == me.id)
        .first()
    )

    if d.owner_id != me.id and not es_colaborador:
        raise HTTPException(status_code=403, detail="No tienes acceso a este diagrama")

    # 🔹 Cargar clases con atributos y métodos
    clases = db.query(Clase).filter(Clase.diagram_id == d.id).all()
    clases_out = [ClaseCompletaOut.model_validate(c) for c in clases]

    # 🔹 Cargar relaciones expandidas
    relaciones = db.query(Relacion).filter(Relacion.diagram_id == d.id).all()
    relaciones_out = []
    for r in relaciones:
        relaciones_out.append(
            RelacionOutExpanded.model_validate({
                **r.__dict__,
                "origen": ClaseCompletaOutLight.model_validate(r.origen),
                "destino": ClaseCompletaOutLight.model_validate(r.destino),
            })
        )

    # 🔹 Respuesta completa
    return {
        "id": str(d.id),
        "title": d.title,
        "owner_id": d.owner_id,
        "clases": clases_out,
        "relaciones": relaciones_out,
        "is_owner": (d.owner_id == me.id),
    }

#  Compartir un diagrama con otro usuario
@router.post("/{diagram_id}/share")
def share_diagram(
    diagram_id: UUID,
    user_id: int,
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user),
):
    diagram = db.query(Diagram).filter(Diagram.id == diagram_id, Diagram.owner_id == me.id).first()
    if not diagram:
        raise HTTPException(status_code=404, detail="Diagrama no encontrado o no te pertenece")

    exists = db.query(DiagramCollaborator).filter_by(diagram_id=diagram_id, user_id=user_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="El usuario ya es colaborador")

    collab = DiagramCollaborator(user_id=user_id, diagram_id=diagram_id)
    db.add(collab)
    db.commit()
    return {"message": "✅ Diagrama compartido correctamente", "diagram_id": str(diagram_id), "user_id": user_id}


