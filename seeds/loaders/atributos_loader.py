import os
from app.models.uml import Diagram, Clase, Atributo
from seeds.utils import norm, bool_from_csv, gen_uuid, _csv_open

def load_atributos(db, data_dir):
    path = os.path.join(data_dir, "atributos.csv")
    rdr = _csv_open(path)
    if rdr is None:
        return

    created, updated = 0, 0
    for row in rdr:
        diagram_title = norm(row.get("diagram_title"))
        clase_nombre = norm(row.get("clase_nombre"))
        nombre = norm(row.get("nombre"))
        tipo = norm(row.get("tipo")) or "string"
        requerido = bool_from_csv(row.get("requerido"), False)
        es_primaria = bool_from_csv(row.get("es_primaria"), False)

        if not (diagram_title and clase_nombre and nombre):
            print("[attrs] fila inválida -> skip")
            continue

        diagram = db.query(Diagram).filter(Diagram.title == diagram_title).one_or_none()
        if not diagram:
            print(f"[attrs] ! diagrama no encontrado: {diagram_title} -> skip")
            continue

        clase = db.query(Clase).filter(Clase.diagram_id == diagram.id, Clase.nombre == clase_nombre).one_or_none()
        if not clase:
            print(f"[attrs] ! clase no encontrada: {diagram_title}.{clase_nombre} -> skip")
            continue

        attr = db.query(Atributo).filter(Atributo.clase_id == clase.id, Atributo.nombre == nombre).one_or_none()
        if attr:
            changed = False
            if attr.tipo != tipo: attr.tipo = tipo; changed = True
            if attr.requerido != requerido: attr.requerido = requerido; changed = True
            if attr.es_primaria != es_primaria: attr.es_primaria = es_primaria; changed = True
            if changed:
                updated += 1; print(f"[attrs] ↺ actualizado: {clase_nombre}.{nombre}")
            else:
                print(f"[attrs] = sin cambios: {clase_nombre}.{nombre}")
        else:
            db.add(Atributo(
                id=gen_uuid(None),
                clase_id=clase.id,
                nombre=nombre,
                tipo=tipo,
                requerido=requerido,
                es_primaria=es_primaria,
            ))
            created += 1
            print(f"[attrs] + creado: {clase_nombre}.{nombre}")

    print(f"[attrs] creado={created}, actualizado={updated}")

if __name__ == "__main__":
    from app.db import SessionLocal
    db = SessionLocal()
    DATA_DIR = "seeds/data"

    print("== Cargando atributos.csv ==")
    load_atributos(db, DATA_DIR)
    db.commit()
    db.close()
    print("✅ Carga de atributos completada.")
