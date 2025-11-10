# app/services/servicio_importacion.py
from app.models.uml import Diagram, Clase, Atributo, Metodo, Relacion, RelType
from sqlalchemy.orm import Session
import uuid

def importar_json_a_bd(data: dict, db: Session, owner_id: int):
    """
    📥 Inserta en la base de datos el contenido de un JSON UML generado por la IA.
    Crea Diagram, Clase, Atributo, Metodo y Relacion con sus multiplicidades y etiquetas.
    """

    # =========================
    # 1️⃣ Verificar estructura
    # =========================
    if "diagram" not in data:
        raise ValueError("Formato de JSON inválido. Falta clave 'diagram'.")

    diagram_data = data["diagram"]

    # =========================
    # 2️⃣ Crear Diagrama
    # =========================
    nuevo_diagrama = Diagram(
        id=uuid.uuid4(),
        title=diagram_data.get("title", "Diagrama sin título"),
        owner_id=owner_id
    )
    db.add(nuevo_diagrama)
    db.commit()
    db.refresh(nuevo_diagrama)

    print(f"🆕 Diagrama creado: {nuevo_diagrama.title}")

    clase_map = {}

    # =========================
    # 3️⃣ Crear Clases
    # =========================
    # for clase_data in diagram_data.get("classes", []):
    #     nueva_clase = Clase(
    #         id=uuid.uuid4(),
    #         nombre=clase_data["name"],
    #         diagram_id=nuevo_diagrama.id
    #     )
    #     db.add(nueva_clase)
    #     db.commit()
    #     db.refresh(nueva_clase)

    #     clase_map[clase_data["name"]] = nueva_clase.id
    #     print(f"   🧱 Clase: {nueva_clase.nombre}")

    #     # --- Atributos ---
    #     for attr_data in clase_data.get("attributes", []):
    #         nuevo_atributo = Atributo(
    #             id=uuid.uuid4(),
    #             nombre=attr_data.get("name"),
    #             tipo=attr_data.get("type", "String"),
    #             requerido=attr_data.get("required", False),
    #             es_primaria=attr_data.get("es_primaria", False),
    #             clase_id=nueva_clase.id
    #         )
    #         db.add(nuevo_atributo)
    #     db.commit()

    #     # --- Métodos ---
    #     for metodo_data in clase_data.get("methods", []):
    #         nuevo_metodo = Metodo(
    #             id=uuid.uuid4(),
    #             nombre=metodo_data.get("name"),
    #             tipo_retorno=metodo_data.get("tipo_retorno", "void"),
    #             clase_id=nueva_clase.id
    #         )
    #         db.add(nuevo_metodo)
    #     db.commit()
    # # =========================
    # # 3️⃣ Crear Clases (con posiciones)
    # # =========================
    # for i, clase_data in enumerate(diagram_data.get("classes", [])):
    #     # Posiciones proporcionadas por la IA (si existen)
    #     x_ia = clase_data.get("x")
    #     y_ia = clase_data.get("y")

    #     # Si la IA no detecta posiciones, se asignan en grilla
    #     if x_ia is None or y_ia is None:
    #         x_ia = (i % 5) * 8   # 5 columnas, 8 unidades de separación
    #         y_ia = (i // 5) * 6  # cada 5 clases, baja una fila

    #     nueva_clase = Clase(
    #         id=uuid.uuid4(),
    #         nombre=clase_data["name"],
    #         diagram_id=nuevo_diagrama.id,
    #         x_grid=x_ia,
    #         y_grid=y_ia,
    #         w_grid=clase_data.get("w", 12),
    #         h_grid=clase_data.get("h", 6),
    #         z_index=clase_data.get("z", 0)
    #     )

    #     db.add(nueva_clase)
    #     db.commit()
    #     db.refresh(nueva_clase)

    #     clase_map[clase_data["name"]] = nueva_clase.id
    #     print(f"   🧱 Clase: {nueva_clase.nombre} en ({x_ia}, {y_ia})")

    #     # --- Atributos ---
    #     for attr_data in clase_data.get("attributes", []):
    #         nuevo_atributo = Atributo(
    #             id=uuid.uuid4(),
    #             nombre=attr_data.get("name"),
    #             tipo=attr_data.get("type", "String"),
    #             requerido=attr_data.get("required", False),
    #             es_primaria=attr_data.get("es_primaria", False),
    #             clase_id=nueva_clase.id
    #         )
    #         db.add(nuevo_atributo)
    #     db.commit()

    #     # --- Métodos ---
    #     for metodo_data in clase_data.get("methods", []):
    #         nuevo_metodo = Metodo(
    #             id=uuid.uuid4(),
    #             nombre=metodo_data.get("name"),
    #             tipo_retorno=metodo_data.get("tipo_retorno", "void"),
    #             clase_id=nueva_clase.id
    #         )
    #         db.add(nuevo_metodo)
    #     db.commit()

    # =========================
    # 3️⃣ Crear Clases (con posiciones inteligentes)
    # =========================
    # Configuración base del grid
    MAX_X = 80
    MAX_Y = 50
    SEP_X = 12   # separación horizontal
    SEP_Y = 8    # separación vertical
    COLS = 6     # clases por fila

    for i, clase_data in enumerate(diagram_data.get("classes", [])):
        # Posiciones detectadas por IA
        x_ia = clase_data.get("x")
        y_ia = clase_data.get("y")

        # Si la IA no las da, se generan automáticas en grilla
        if x_ia is None or y_ia is None:
            col = i % COLS
            row = i // COLS
            x_ia = min(col * SEP_X, MAX_X - 10)
            y_ia = min(row * SEP_Y, MAX_Y - 6)

        nueva_clase = Clase(
            id=uuid.uuid4(),
            nombre=clase_data["name"],
            diagram_id=nuevo_diagrama.id,
            x_grid=int(x_ia),
            y_grid=int(y_ia),
            w_grid=int(clase_data.get("w", 12)),
            h_grid=int(clase_data.get("h", 6)),
            z_index=int(clase_data.get("z", 0))
        )

        db.add(nueva_clase)
        db.commit()
        db.refresh(nueva_clase)

        clase_map[clase_data["name"]] = nueva_clase.id
        print(f"   🧱 Clase: {nueva_clase.nombre} → ({x_ia}, {y_ia})")

        # --- Atributos ---
        for attr_data in clase_data.get("attributes", []):
            nuevo_atributo = Atributo(
                id=uuid.uuid4(),
                nombre=attr_data.get("name"),
                tipo=attr_data.get("type", "String"),
                requerido=attr_data.get("required", False),
                es_primaria=attr_data.get("es_primaria", False),
                clase_id=nueva_clase.id
            )
            db.add(nuevo_atributo)
        db.commit()

        # --- Métodos ---
        for metodo_data in clase_data.get("methods", []):
            nuevo_metodo = Metodo(
                id=uuid.uuid4(),
                nombre=metodo_data.get("name"),
                tipo_retorno=metodo_data.get("tipo_retorno", "void"),
                clase_id=nueva_clase.id
            )
            db.add(nuevo_metodo)
        db.commit()
    # =========================
    # 4️⃣ Crear Relaciones
    # =========================

    def parse_mult(v):
        """Convierte multiplicidades UML ('*', 'N', '1', etc.) a enteros válidos."""
        if v is None:
            return None
        v = str(v).strip()
        if v in ["*", "N", "n", "many", "∞"]:
            return -1  # usamos -1 para representar "muchos"
        try:
            return int(v)
        except ValueError:
            return None

    for rel_data in diagram_data.get("relations", []):
        origen_nombre = rel_data.get("from")
        destino_nombre = rel_data.get("to")
        if not origen_nombre or not destino_nombre:
            print("⚠️ Relación omitida: falta origen o destino.")
            continue

        origen_id = clase_map.get(origen_nombre)
        destino_id = clase_map.get(destino_nombre)
        if not origen_id or not destino_id:
            print(f"⚠️ No se encontró clase para relación: {origen_nombre} → {destino_nombre}")
            continue

        try:
            tipo_rel = RelType(rel_data.get("type", "ASSOCIATION"))
        except ValueError:
            tipo_rel = RelType.ASSOCIATION  # valor por defecto

        nueva_rel = Relacion(
            id=uuid.uuid4(),
            diagram_id=nuevo_diagrama.id,
            origen_id=origen_id,
            destino_id=destino_id,
            tipo=tipo_rel,
            etiqueta=rel_data.get("label", None),
            mult_origen_min=parse_mult(rel_data.get("from_min")),
            mult_origen_max=parse_mult(rel_data.get("from_max")),
            mult_destino_min=parse_mult(rel_data.get("to_min")),
            mult_destino_max=parse_mult(rel_data.get("to_max"))
        )
        db.add(nueva_rel)
        print(f"   🔗 Relación: {origen_nombre} → {destino_nombre} ({tipo_rel.value}) "
              f"[{rel_data.get('from_min','?')}..{rel_data.get('from_max','?')} → {rel_data.get('to_min','?')}..{rel_data.get('to_max','?')}]")

    db.commit()
    print("✅ Importación completa.")
    return {"ok": True, "diagrama_id": str(nuevo_diagrama.id), "title": nuevo_diagrama.title}
