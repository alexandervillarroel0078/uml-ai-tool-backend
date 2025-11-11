# # app/routes/flutter_export.py
# import os, sys, zipfile
# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.responses import FileResponse
# from sqlalchemy.orm import Session
# from uuid import UUID

# from app.db import get_db
# from app.models.uml import Diagram

# # ============================
# # 📁 Configuración de rutas
# # ============================

# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
# sys.path.append(PROJECT_ROOT)

# EXPORT_DIR = os.path.join(PROJECT_ROOT, "exporters", "json")
# FLUTTER_OUTPUT = os.path.join(PROJECT_ROOT, "exportersFlutter", "APPGENERADA", "flutter_app")
# os.makedirs(EXPORT_DIR, exist_ok=True)

# # ============================
# # 📦 Importar generador Flutter
# # ============================

# from exportersFlutter.generators.flutter_generator import generate_from_json
# from exporters.generators.uml_to_json import export_diagram_to_json
# from exporters.generators.validator import UMLValidationError

# router = APIRouter(prefix="/diagrams", tags=["Flutter Export"])

# # ============================
# # 🧩 Función: armar JSON UML
# # ============================

# def build_diagram_dict(diagram: Diagram) -> dict:
#     return {
#         "id": str(diagram.id),
#         "title": diagram.title,
#         "classes": [
#             {
#                 "id": str(c.id),
#                 "name": c.nombre,
#                 "attributes": [
#                     {"name": a.nombre, "type": a.tipo, "required": a.requerido, "es_primaria": a.es_primaria}
#                     for a in c.atributos
#                 ],
#                 "methods": [
#                     {"name": m.nombre, "return_type": m.tipo_retorno}
#                     for m in c.metodos
#                 ],
#             }
#             for c in diagram.classes
#         ],
#         "relations": [
#             {
#                 "from": r.origen.nombre,
#                 "from_id": str(r.origen_id),
#                 "to": r.destino.nombre,
#                 "to_id": str(r.destino_id),
#                 "type": r.tipo.value,
#                 "from_min": r.mult_origen_min,
#                 "from_max": r.mult_origen_max,
#                 "to_min": r.mult_destino_min,
#                 "to_max": r.mult_destino_max,
#                 "label": r.etiqueta or "",
#                 "role_from": r.origen.nombre.lower(),
#                 "role_to": r.destino.nombre.lower(),
#             }
#             for r in diagram.relations
#         ],
#     }

# # ============================
# # 🗜️ Comprimir proyecto
# # ============================

# def zip_flutter_project(output_dir: str, zip_path: str):
#     if os.path.exists(zip_path):
#         os.remove(zip_path)
#     with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
#         for root, _, files in os.walk(output_dir):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 arcname = os.path.relpath(file_path, output_dir)
#                 zipf.write(file_path, arcname)
#     return zip_path

# # ============================
# # 🚀 Endpoint principal
# # ============================

# @router.post("/{diagram_id}/export-flutter")
# def export_flutter(diagram_id: UUID, db: Session = Depends(get_db)):
#     diagram = db.query(Diagram).filter(Diagram.id == diagram_id).first()
#     if not diagram:
#         raise HTTPException(404, "Diagrama no encontrado")

#     json_path = os.path.join(EXPORT_DIR, f"diagram_{diagram_id}.json")
#     zip_path = os.path.join(EXPORT_DIR, f"flutter_app_{diagram_id}.zip")

#     try:
#         # 1️⃣ Guardar JSON UML
#         diagram_dict = build_diagram_dict(diagram)
#         export_diagram_to_json(diagram_dict, json_path)

#         # 2️⃣ Generar proyecto Flutter
#         generate_from_json(json_path)

#         # 3️⃣ Comprimir en ZIP
#         zip_flutter_project(FLUTTER_OUTPUT, zip_path)

#         # 4️⃣ Descargar directamente el ZIP
#         return FileResponse(
#             zip_path,
#             media_type="application/zip",
#             filename=f"flutter_app_{diagram_id}.zip"
#         )

#     except UMLValidationError as e:
#         raise HTTPException(status_code=400, detail=f"Error de validación UML: {e}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error interno: {e}")
# app/routes/flutter_export.py
import os, sys, zipfile
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from uuid import UUID

from app.db import get_db
from app.models.uml import Diagram

# ============================
# 📁 Configuración de rutas
# ============================
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(PROJECT_ROOT)

EXPORT_DIR = os.path.join(PROJECT_ROOT, "exporters", "json")
FLUTTER_OUTPUT = os.path.join(PROJECT_ROOT, "uml-ai-tool-backend", "exportersFlutter", "APPGENERADA", "flutter_app")
print(f"📁 FLUTTER_OUTPUT real: {FLUTTER_OUTPUT}")
os.makedirs(EXPORT_DIR, exist_ok=True)

# ============================
# 📦 Importar generador Flutter
# ============================
from exportersFlutter.generators.flutter_generator import generate_from_json
from exporters.generators.uml_to_json import export_diagram_to_json
from exporters.generators.validator import UMLValidationError

router = APIRouter(prefix="/diagrams", tags=["Flutter Export"])

# ============================
# 🧩 Función: armar JSON UML
# ============================
def build_diagram_dict(diagram: Diagram) -> dict:
    return {
        "id": str(diagram.id),
        "title": diagram.title,
        "classes": [
            {
                "id": str(c.id),
                "name": c.nombre,
                "attributes": [
                    {"name": a.nombre, "type": a.tipo, "required": a.requerido, "es_primaria": a.es_primaria}
                    for a in c.atributos
                ],
                "methods": [
                    {"name": m.nombre, "return_type": m.tipo_retorno}
                    for m in c.metodos
                ],
            }
            for c in diagram.classes
        ],
        "relations": [
            {
                "from": r.origen.nombre,
                "from_id": str(r.origen_id),
                "to": r.destino.nombre,
                "to_id": str(r.destino_id),
                "type": r.tipo.value,
                "from_min": r.mult_origen_min,
                "from_max": r.mult_origen_max,
                "to_min": r.mult_destino_min,
                "to_max": r.mult_destino_max,
                "label": r.etiqueta or "",
                "role_from": r.origen.nombre.lower(),
                "role_to": r.destino.nombre.lower(),
            }
            for r in diagram.relations
        ],
    }

# ============================
# 🗜️ Comprimir proyecto
# ============================
def zip_flutter_project(output_dir: str, zip_path: str):
    if os.path.exists(zip_path):
        os.remove(zip_path)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_dir)
                zipf.write(file_path, arcname)
    return zip_path

# ============================
# 🚀 Endpoint principal
# ============================
@router.post("/{diagram_id}/export-flutter")
def export_flutter(diagram_id: UUID, db: Session = Depends(get_db)):
    print(f"🦋 [EXPORT-FLUTTER] Iniciando exportación para diagrama {diagram_id}")
    diagram = db.query(Diagram).filter(Diagram.id == diagram_id).first()
    if not diagram:
        print("❌ Diagrama no encontrado en la BD.")
        raise HTTPException(404, "Diagrama no encontrado")

    json_path = os.path.join(EXPORT_DIR, f"diagram_{diagram_id}.json")
    zip_path = os.path.join(EXPORT_DIR, f"flutter_app_{diagram_id}.zip")

    try:
        # 1️⃣ Guardar JSON UML
        print("📄 Generando JSON UML...")
        diagram_dict = build_diagram_dict(diagram)
        export_diagram_to_json(diagram_dict, json_path)
        print(f"✅ JSON generado: {json_path}")

        # 2️⃣ Generar proyecto Flutter
        print("⚙️ Ejecutando generador Flutter...")
        generate_from_json(json_path)
        print(f"✅ Proyecto Flutter generado en {FLUTTER_OUTPUT}")

        # 3️⃣ Comprimir en ZIP
        print("🗜️ Comprimiendo proyecto Flutter...")
        zip_flutter_project(FLUTTER_OUTPUT, zip_path)
        print(f"✅ ZIP creado: {zip_path}")

        # 4️⃣ Verificar existencia antes de devolver
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"ZIP no encontrado: {zip_path}")

        print("📦 Enviando archivo ZIP al cliente...")
        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename=f"flutter_app_{diagram_id}.zip"
        )

    except UMLValidationError as e:
        print(f"❌ Error de validación UML: {e}")
        raise HTTPException(status_code=400, detail=f"Error de validación UML: {e}")
    except Exception as e:
        print(f"💥 Error interno en exportación Flutter: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")
