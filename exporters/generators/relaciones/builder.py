#exporters/generators/relaciones/builder.py
"""
builder.py
Coordina la construcción del mapa de relaciones UML → JPA.
"""

import json
from exporters.generators.relaciones.herencia_handler import handle_inheritance
from exporters.generators.relaciones.composicion_handler import handle_composition
from exporters.generators.relaciones.agregacion_handler import handle_aggregation
from exporters.generators.relaciones.dependencia_handler import handle_dependency
from exporters.generators.relaciones.asociacion_handler import handle_association
from exporters.generators.relaciones.helpers import to_camel


def build_relations(json_path: str):
    """Construye el mapa de relaciones entre clases UML basadas en el JSON exportado."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    relations_map = {}
    diagram = data["diagram"]

    for rel in diagram["relations"]:
        rel_type = rel["type"]

        if rel_type == "INHERITANCE":
            handle_inheritance(rel, relations_map)
        elif rel_type == "COMPOSITION":
            handle_composition(rel, relations_map)
        elif rel_type == "AGGREGATION":
            handle_aggregation(rel, relations_map)
        elif rel_type == "DEPENDENCY":
            handle_dependency(rel, relations_map)
        elif rel_type == "ASSOCIATION":
            handle_association(rel, relations_map)

    return relations_map
