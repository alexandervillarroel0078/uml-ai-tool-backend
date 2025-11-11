#exporters/generators/relaciones/herencia_handler.py
"""
herencia_handler.py
Gestiona las relaciones de tipo INHERITANCE.

"""

def handle_inheritance(rel, relations_map):
    src = rel["from"]
    dst = rel["to"]
    hijo, padre = src, dst

    relations_map.setdefault(hijo, {})
    relations_map.setdefault(padre, {})

    relations_map[hijo][padre] = {
        "type": "Extends",
        "parent": padre
    }

    relations_map[padre][hijo] = {
        "type": "Inheritance",
        "annotation": "@Inheritance(strategy = InheritanceType.JOINED)"
    }
