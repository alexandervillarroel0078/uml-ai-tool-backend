# import os
# from app.models.uml import Diagram, Clase
# from seeds.utils import norm, gen_uuid, _csv_open

# def load_clases(db, data_dir):
#     path = os.path.join(data_dir, "clases.csv")
#     rdr = _csv_open(path)
#     if rdr is None:
#         return

#     created, existing = 0, 0
#     for row in rdr:
#         id_raw = norm(row.get("id"))
#         diagram_title = norm(row.get("diagram_title"))
#         nombre = norm(row.get("nombre"))

#         if not diagram_title or not nombre:
#             print("[clases] fila inválida -> skip")
#             continue

#         diagram = db.query(Diagram).filter(Diagram.title == diagram_title).one_or_none()
#         if not diagram:
#             print(f"[clases] ! diagrama no encontrado: {diagram_title} -> skip")
#             continue

#         clase = db.query(Clase).filter(Clase.diagram_id == diagram.id, Clase.nombre == nombre).one_or_none()
#         if clase:
#             existing += 1
#             print(f"[clases] = sin cambios: {diagram_title}.{nombre}")
#         else:
#             db.add(Clase(id=gen_uuid(id_raw), nombre=nombre, diagram_id=diagram.id))
#             created += 1
#             print(f"[clases] + creada: {diagram_title}.{nombre}")

#     print(f"[clases] creado={created}, existente={existing}")


# # -----------------------------------------------------------
# # 👇 Bloque para ejecutar este loader directamente
# # Ejemplo: python -m seeds.loaders.clases_loader
# # -----------------------------------------------------------
# if __name__ == "__main__":
#     from app.db import SessionLocal
#     db = SessionLocal()
#     DATA_DIR = "seeds/data"

#     print("== Cargando clases.csv ==")
#     load_clases(db, DATA_DIR)
#     db.commit()
#     db.close()
#     print("✅ Carga de clases completada.")
import os
from app.models.uml import Diagram, Clase
from seeds.utils import norm, gen_uuid, _csv_open

def load_clases(db, data_dir):
    path = os.path.join(data_dir, "clases.csv")
    rdr = _csv_open(path)
    if rdr is None:
        return

    created, updated, existing = 0, 0, 0
    for row in rdr:
        id_raw = norm(row.get("id"))
        diagram_title = norm(row.get("diagram_title"))
        nombre = norm(row.get("nombre"))

        # Layout
        x_grid = int(row.get("x_grid") or 0)
        y_grid = int(row.get("y_grid") or 0)
        w_grid = int(row.get("w_grid") or 12)
        h_grid = int(row.get("h_grid") or 6)
        z_index = int(row.get("z_index") or 0)

        if not diagram_title or not nombre:
            print("[clases] fila inválida -> skip")
            continue

        diagram = db.query(Diagram).filter(Diagram.title == diagram_title).one_or_none()
        if not diagram:
            print(f"[clases] ! diagrama no encontrado: {diagram_title} -> skip")
            continue

        clase = db.query(Clase).filter(Clase.diagram_id == diagram.id, Clase.nombre == nombre).one_or_none()
        if clase:
            changed = False
            if (clase.x_grid, clase.y_grid, clase.w_grid, clase.h_grid, clase.z_index) != (x_grid, y_grid, w_grid, h_grid, z_index):
                clase.x_grid, clase.y_grid, clase.w_grid, clase.h_grid, clase.z_index = x_grid, y_grid, w_grid, h_grid, z_index
                updated += 1
                changed = True
                print(f"[clases] ↺ posición actualizada: {diagram_title}.{nombre}")
            if not changed:
                existing += 1
                print(f"[clases] = sin cambios: {diagram_title}.{nombre}")
        else:
            db.add(Clase(
                id=gen_uuid(id_raw),
                nombre=nombre,
                diagram_id=diagram.id,
                x_grid=x_grid,
                y_grid=y_grid,
                w_grid=w_grid,
                h_grid=h_grid,
                z_index=z_index,
            ))
            created += 1
            print(f"[clases] + creada: {diagram_title}.{nombre}")

    print(f"[clases] creado={created}, actualizado={updated}, existente={existing}")


if __name__ == "__main__":
    from app.db import SessionLocal
    db = SessionLocal()
    DATA_DIR = "seeds/data"

    print("== Cargando clases.csv ==")
    load_clases(db, DATA_DIR)
    db.commit()
    db.close()
    print("✅ Carga de clases completada.")
