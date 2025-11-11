"""
manejador_herencia.py
Detecta si una clase UML tiene herencia (extends) o anotaciones @Inheritance.
"""

def detectar_herencia(nombre_clase: str, relaciones: dict):
    """Devuelve (padre, anotación) si la clase hereda o usa herencia JPA."""
    clase_padre = None
    anotacion = None

    if nombre_clase in relaciones:
        for destino, rel in relaciones[nombre_clase].items():
            if rel["type"] == "Inheritance":
                anotacion = rel["annotation"]
            elif rel["type"] == "Extends":
                clase_padre = rel["parent"]

    return clase_padre, anotacion
