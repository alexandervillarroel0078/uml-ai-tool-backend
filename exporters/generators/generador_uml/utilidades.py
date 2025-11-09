"""
utilidades.py
Contiene funciones pequeñas y reutilizables del generador.
"""

def a_camel(nombre: str) -> str:
    """Convierte un texto a formato camelCase."""
    if not nombre:
        return nombre
    return nombre[0].lower() + nombre[1:]
