import os
from app.models.user import User
from app.models.uml import Diagram
from seeds.utils import norm, gen_uuid, _csv_open

def load_diagrams(db, data_dir):
    path = os.path.join(data_dir, "diagrams.csv")
    rdr = _csv_open(path)
    if rdr is None:
        return

    created, updated = 0, 0
    for row in rdr:
        id_raw = norm(row.get("id"))
        title = norm(row.get("title"))
        owner_email = norm(row.get("owner_email")).lower()

        if not title or not owner_email:
            print("[diagrams] fila inválida -> skip")
            continue

        owner = db.query(User).filter(User.email == owner_email).one_or_none()
        if not owner:
            print(f"[diagrams] ! owner no encontrado: {owner_email} -> skip")
            continue

        diagram = db.query(Diagram).filter(Diagram.title == title).one_or_none()
        if diagram:
            if diagram.owner_id != owner.id:
                diagram.owner_id = owner.id
                updated += 1
                print(f"[diagrams] ↺ actualizado: {title}")
            else:
                print(f"[diagrams] = sin cambios: {title}")
        else:
            db.add(Diagram(id=gen_uuid(id_raw), title=title, owner_id=owner.id))
            created += 1
            print(f"[diagrams] + creado: {title}")

    print(f"[diagrams] creado={created}, actualizado={updated}")

# -----------------------------------------------------------
# 👇 Bloque para ejecutar este loader directamente
# Ejemplo: python -m seeds.loaders.diagrams_loader
# -----------------------------------------------------------
if __name__ == "__main__":
    from app.db import SessionLocal
    db = SessionLocal()
    DATA_DIR = "seeds/data"

    print("== Cargando diagrams.csv ==")
    load_diagrams(db, DATA_DIR)
    db.commit()
    db.close()
    print("✅ Carga de diagrams completada.")
