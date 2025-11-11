# #exporters/generators/relaciones/agregacion_handler.py
# """
# agregacion_handler.py
# Gestiona relaciones de tipo AGGREGATION (1:N débil).
# """

# from exporters.generators.relaciones.helpers import to_camel

# def handle_aggregation(rel, relations_map):
#     padre = rel["to"]
#     hijo = rel["from"]

#     relations_map.setdefault(padre, {})
#     relations_map.setdefault(hijo, {})

#     relations_map[padre][hijo] = {
#         "type": "Aggregation",
#         "annotation": "@OneToMany",
#         "mappedBy": to_camel(padre)
#     }

#     relations_map[hijo][padre] = {
#         "type": "Aggregation",
#         "annotation": "@ManyToOne",
#         "joinColumn": f"{to_camel(padre)}_id"
#     }
# exporters/generators/relaciones/agregacion_handler.py
"""
agregacion_handler.py
Maneja relaciones UML de tipo AGGREGATION (relación débil 1:N).
Ejemplo: Un Departamento tiene muchos Empleados.
"""

from exporters.generators.relaciones.helpers import to_camel

def handle_aggregation(rel, relations_map):
    """Construye relación AGGREGATION → genera @OneToMany / @ManyToOne."""
    from_class = rel["from"]   # Hijo (Empleado)
    to_class = rel["to"]       # Padre (Departamento)

    # Asegurar que existan los diccionarios base
    relations_map.setdefault(from_class, {})
    relations_map.setdefault(to_class, {})

    # --- 1️⃣ Lado 'padre' (Departamento) ---
    # Un departamento tiene muchos empleados
    relations_map[to_class][from_class] = {
        "type": "OneToMany",
        "annotation": "@OneToMany",
        "mappedBy": to_camel(to_class),
        "label": rel.get("label") or f"{to_camel(from_class)}s"
    }

    # --- 2️⃣ Lado 'hijo' (Empleado) ---
    # Un empleado pertenece a un departamento
    relations_map[from_class][to_class] = {
        "type": "ManyToOne",
        "annotation": "@ManyToOne",
        "joinColumn": f"{to_camel(to_class)}_id",
        "label": rel.get("role_to") or to_camel(to_class)
    }
