import os
from app.models.uml import Diagram, Clase, Relacion, RelType
from seeds.utils import norm, gen_uuid, _csv_open


def load_relaciones(db, data_dir):
    """
    Carga las relaciones desde relaciones.csv (usando nombres de diagrama y clase).
    """
    path = os.path.join(data_dir, "relaciones.csv")
    rdr = _csv_open(path)
    if rdr is None:
        return

    created, updated = 0, 0
    for row in rdr:
        diagram_title = norm(row.get("diagram_title"))
        clase_origen = norm(row.get("clase_origen"))
        clase_destino = norm(row.get("clase_destino"))
        tipo_str = norm(row.get("tipo"))
        etiqueta = norm(row.get("etiqueta"))

        # 🧩 Anchors (direcciones visuales)
        src_anchor = norm(row.get("src_anchor") or "right")
        dst_anchor = norm(row.get("dst_anchor") or "left")

        if not (diagram_title and clase_origen and clase_destino and tipo_str):
            print("[rels] fila inválida -> skip")
            continue

        diagram = db.query(Diagram).filter(Diagram.title == diagram_title).one_or_none()
        if not diagram:
            print(f"[rels] ! diagrama no encontrado: {diagram_title} -> skip")
            continue

        origen = db.query(Clase).filter(
            Clase.diagram_id == diagram.id, Clase.nombre == clase_origen
        ).one_or_none()

        destino = db.query(Clase).filter(
            Clase.diagram_id == diagram.id, Clase.nombre == clase_destino
        ).one_or_none()

        if not origen or not destino:
            print(f"[rels] ! clase origen/destino no encontrada: {clase_origen} -> {clase_destino} -> skip")
            continue

        try:
            tipo_enum = RelType[tipo_str.upper()]
        except KeyError:
            print(f"[rels] ! tipo inválido: {tipo_str}")
            continue

        # 🔎 Buscar si ya existe
        rel = db.query(Relacion).filter(
            Relacion.diagram_id == diagram.id,
            Relacion.origen_id == origen.id,
            Relacion.destino_id == destino.id,
            Relacion.tipo == tipo_enum
        ).one_or_none()

        mult_origen_min = int(row.get("mult_origen_min", 1))
        mult_origen_max = None if row.get("mult_origen_max") in ("", "NULL", None, "*") else int(row["mult_origen_max"])
        mult_destino_min = int(row.get("mult_destino_min", 1))
        mult_destino_max = None if row.get("mult_destino_max") in ("", "NULL", None, "*") else int(row["mult_destino_max"])

        if rel:
            changed = False
            if rel.etiqueta != etiqueta: rel.etiqueta = etiqueta; changed = True
            if rel.mult_origen_min != mult_origen_min: rel.mult_origen_min = mult_origen_min; changed = True
            if rel.mult_origen_max != mult_origen_max: rel.mult_origen_max = mult_origen_max; changed = True
            if rel.mult_destino_min != mult_destino_min: rel.mult_destino_min = mult_destino_min; changed = True
            if rel.mult_destino_max != mult_destino_max: rel.mult_destino_max = mult_destino_max; changed = True
            if rel.src_anchor != src_anchor: rel.src_anchor = src_anchor; changed = True
            if rel.dst_anchor != dst_anchor: rel.dst_anchor = dst_anchor; changed = True

            if changed:
                updated += 1
                print(f"[rels] ↺ actualizado: {clase_origen} -> {clase_destino} ({tipo_str}) [{src_anchor}→{dst_anchor}]")
            else:
                print(f"[rels] = sin cambios: {clase_origen} -> {clase_destino}")
        else:
            db.add(Relacion(
                id=gen_uuid(None),
                diagram_id=diagram.id,
                origen_id=origen.id,
                destino_id=destino.id,
                tipo=tipo_enum,
                etiqueta=etiqueta,
                mult_origen_min=mult_origen_min,
                mult_origen_max=mult_origen_max,
                mult_destino_min=mult_destino_min,
                mult_destino_max=mult_destino_max,
                src_anchor=src_anchor,
                dst_anchor=dst_anchor,
            ))
            created += 1
            print(f"[rels] + creada: {clase_origen} -> {clase_destino} ({tipo_str}) [{src_anchor}→{dst_anchor}]")

    print(f"[rels] creado={created}, actualizado={updated}")


if __name__ == "__main__":
    from app.db import SessionLocal
    db = SessionLocal()
    DATA_DIR = "seeds/data"

    print("== Cargando relaciones.csv ==")
    load_relaciones(db, DATA_DIR)
    db.commit()
    db.close()
    print("✅ Carga de relaciones completada.")
