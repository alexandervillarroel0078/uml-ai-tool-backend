# #exporters/generators/relaciones/dependencia_handler.py
# """
# dependencia_handler.py
# Gestiona relaciones de tipo DEPENDENCY (1:1 débil o dependencia directa).
# """

# from exporters.generators.relaciones.helpers import to_camel

# def handle_dependency(rel, relations_map):
#     padre = rel["to"]
#     hijo = rel["from"]

#     relations_map.setdefault(padre, {})
#     relations_map.setdefault(hijo, {})

#     relations_map[hijo][padre] = {
#         "type": "Dependency",
#         "annotation": "@OneToOne",
#         "joinColumn": f"{to_camel(padre)}_id"
#     }

#     relations_map[padre][hijo] = {
#         "type": "Dependency",
#         "annotation": f"@OneToOne(mappedBy = \"{to_camel(padre)}\")"
#     }
"""
dependencia_handler.py
Gestiona relaciones de tipo DEPENDENCY (1:1 o N:1 débil, sin cascada).
El lado 'from' (hijo) depende del 'to' (padre).
"""

from exporters.generators.relaciones.helpers import to_camel

def handle_dependency(rel, relations_map):
    dependiente = rel["from"]   # Ej: Factura
    depende_de = rel["to"]      # Ej: Pedido

    relations_map.setdefault(dependiente, {})
    relations_map.setdefault(depende_de, {})

    # Lado dependiente: tiene la FK al objeto del que depende
    relations_map[dependiente][depende_de] = {
        "type": "Dependency",
        "annotation": "@OneToOne",
        "joinColumn": f"{to_camel(depende_de)}_id",
        "label": to_camel(depende_de)
    }

    # Lado opuesto: no siempre se modela, pero lo dejamos opcional
    relations_map[depende_de][dependiente] = {
        "type": "DependencyInverse",
        "annotation": f"@OneToOne(mappedBy = \"{to_camel(depende_de)}\")",
        "label": to_camel(dependiente)
    }
