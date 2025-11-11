import re

"""
helpers.py
Funciones utilitarias neutrales (evita importaciones circulares).
Contiene herramientas comunes como `to_camel` y el renderizador de relaciones.
"""

def to_camel(name: str) -> str:
    """Convierte nombres a camelCase: UnidadMedida → unidadMedida."""
    if not name:
        return name
    parts = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])", name)
    parts = [p.lower() for p in parts]
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def to_pascal(name: str) -> str:
    """Convierte nombres a PascalCase (nombre de clase en Java)."""
    if not name:
        return name
    parts = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])", name)
    return "".join(p.capitalize() for p in parts)


def render_relations(nombre_clase: str, relaciones: dict) -> list[str]:
    """
    Genera las líneas Java correspondientes a las relaciones JPA
    usando el mapa construido por los handlers (ya tiene type y annotation).
    """
    lineas = []
    if nombre_clase not in relaciones:
        return lineas

    for destino, rel in relaciones[nombre_clase].items():
        tipo = rel.get("type", "")
        annotation = rel.get("annotation", "")
        join_column = rel.get("joinColumn")
        nombre_var = rel.get("label") or to_camel(destino)

        # 🧠 Ignorar herencia
        if tipo in ("Inheritance", "Extends"):
            continue

        # 🧩 Anotaciones JPA
        if annotation:
            lineas.append(f"    {annotation}")
        if join_column:
            lineas.append(f"    @JoinColumn(name = \"{join_column}\")")

        # 💡 Determinar tipo real de clase destino
        tipo_base = to_pascal(destino.split("_")[0])

        if tipo in ("OneToMany", "ManyToMany"):
            tipo_java = f"List<{tipo_base}>"
        else:
            tipo_java = tipo_base

        # 🧱 Campo Java
        lineas.append(f"    private {tipo_java} {nombre_var};\n")

    return lineas
