# #exporters/generators/relaciones/composicion_handler.py

# """
# composicion_handler.py
# Gestiona relaciones de tipo COMPOSITION (1:N fuerte).
# """

# from exporters.generators.relaciones.helpers import to_camel

# def handle_composition(rel, relations_map):
#     padre = rel["to"]       # Ej: Pedido
#     hijo = rel["from"]      # Ej: DetallePedido

#     relations_map.setdefault(padre, {})
#     relations_map.setdefault(hijo, {})

#     # Padre (Pedido) → lista de hijos (DetallePedido)
#     relations_map[padre][hijo] = {
#         "type": "Composition",
#         "annotation": "@OneToMany(mappedBy = \"" + to_camel(padre) + "\", cascade = CascadeType.ALL, orphanRemoval = true)",
#         "label": f"{to_camel(hijo)}s"
#     }

#     # Hijo (DetallePedido) → referencia al padre (Pedido)
#     relations_map[hijo][padre] = {
#         "type": "Composition",
#         "annotation": "@ManyToOne",
#         "joinColumn": f"{to_camel(padre)}_id",
#         "label": to_camel(padre)
#     }
"""
composicion_handler.py
Gestiona relaciones de tipo COMPOSITION (1:N fuerte).
"""

from exporters.generators.relaciones.helpers import to_camel

def handle_composition(rel, relations_map):
    padre = rel["to"]       # Ej: Pedido
    hijo = rel["from"]      # Ej: DetallePedido

    relations_map.setdefault(padre, {})
    relations_map.setdefault(hijo, {})

    # Padre (Pedido) → lista de hijos (DetallePedido)
    relations_map[padre][hijo] = {
        "type": "OneToMany",  # ✅ Tipo real para Hibernate
        "annotation": f"@OneToMany(mappedBy = \"{to_camel(padre)}\", cascade = CascadeType.ALL, orphanRemoval = true)",
        "label": f"{to_camel(hijo)}s",
        "composition": True   # metadata adicional
    }

    # Hijo (DetallePedido) → referencia al padre (Pedido)
    relations_map[hijo][padre] = {
        "type": "ManyToOne",  # ✅ Tipo real para Hibernate
        "annotation": "@ManyToOne",
        "joinColumn": f"{to_camel(padre)}_id",
        "label": to_camel(padre),
        "composition": True
    }
