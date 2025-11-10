
# app/services/ia_edicion_bd.py
from app.models.uml import Diagram, Clase, Atributo, Relacion, RelType
from sqlalchemy.orm import Session

def aplicar_edicion_a_bd(nuevo_json: dict, db: Session, diagram_id: str):
    """
    Aplica los cambios del JSON modificado a la base de datos
    sin crear un nuevo diagrama (solo actualiza el existente).
    """
    diagram_json = nuevo_json.get("diagram")
    diagram = db.query(Diagram).filter(Diagram.id == diagram_id).first()
    if not diagram:
        raise ValueError("El diagrama no existe")

    # 🧹 Limpiar contenido previo (clases y relaciones)
    for rel in diagram.relations:
        db.delete(rel)
    for c in diagram.classes:
        db.delete(c)
    db.commit()

    # ==========================
    # 🧩 Crear nuevas clases sin superposición
    # ==========================
    x_step, y_step = 14, 8  # separación horizontal y vertical
    max_width = 56          # límite del canvas
    used_positions = set()

    for i, c in enumerate(diagram_json.get("classes", [])):
        # 💡 calcular posición en cuadrícula
        x_pos = (i * x_step) % max_width
        y_pos = (i // (max_width // x_step)) * y_step

        # asegurar que no haya dos clases en misma posición
        while (x_pos, y_pos) in used_positions:
            x_pos += x_step
            if x_pos >= max_width:
                x_pos = 0
                y_pos += y_step

        used_positions.add((x_pos, y_pos))

        clase = Clase(
            nombre=c["name"],
            diagram_id=diagram.id,
            x_grid=x_pos,
            y_grid=y_pos,
            w_grid=12,
            h_grid=6,
        )
        db.add(clase)
        db.commit()
        db.refresh(clase)

        # Atributos
        for a in c.get("attributes", []):
            atributo = Atributo(
                nombre=a["name"],
                tipo=a.get("type", "string"),
                requerido=a.get("requerido", False),
                es_primaria=a.get("es_primaria", False),
                clase_id=clase.id,
            )
            db.add(atributo)

    db.commit()

    # 🔗 Crear relaciones
    for r in diagram_json.get("relations", []):
        origen = (
            db.query(Clase)
            .filter(Clase.nombre == r.get("from"), Clase.diagram_id == diagram.id)
            .first()
        )
        destino = (
            db.query(Clase)
            .filter(Clase.nombre == r.get("to"), Clase.diagram_id == diagram.id)
            .first()
        )

        if not origen or not destino:
            print(
                f"⚠️ Relación ignorada: {r.get('from')} → {r.get('to')} (clase no encontrada)"
            )
            continue

        # 🧠 Tipo de relación (si no está, se asume ASSOCIATION)
        tipo_raw = str(r.get("type", "ASSOCIATION")).upper().strip()
        if tipo_raw not in RelType.__members__:
            tipo_raw = "ASSOCIATION"

        # 🧩 Multiplicidad flexible
        # acepta: multiplicity.from / multiplicity_from o multiplicity_to
        mult = r.get("multiplicity", {})
        m_from = (
            str(mult.get("from"))
            if "multiplicity" in r
            else str(r.get("multiplicity_from", "1"))
        ).upper()
        m_to = (
            str(mult.get("to"))
            if "multiplicity" in r
            else str(r.get("multiplicity_to", "1"))
        ).upper()

        # ⚙️ Si no hay multiplicidad clara, se interpreta 1:N por defecto
        if not m_from or not m_to:
            m_from, m_to = "1", "N"

        # 🧩 Convertir N, * o M en 1..*
        def parse_mult(value):
            if value in ["N", "*", "M"]:
                return (1, None)  # 1..*
            elif ".." in value:  # formato "0..1" o "1..N"
                parts = value.split("..")
                min_ = int(parts[0]) if parts[0].isdigit() else 0
                max_ = int(parts[1]) if parts[1].isdigit() else None
                return (min_, max_)
            elif value.isdigit():
                num = int(value)
                return (num, num)
            return (1, None)

        origen_min, origen_max = parse_mult(m_from)
        destino_min, destino_max = parse_mult(m_to)

        rel = Relacion(
            diagram_id=diagram.id,
            origen_id=origen.id,
            destino_id=destino.id,
            tipo=RelType[tipo_raw],
            mult_origen_min=origen_min,
            mult_origen_max=origen_max,
            mult_destino_min=destino_min,
            mult_destino_max=destino_max,
        )
        db.add(rel)



    db.commit()
    return diagram
