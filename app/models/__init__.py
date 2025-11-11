#models/__init__.py
from .uml import Diagram, Clase, Relacion, Atributo, Metodo
from .user import User
from .collaborator import DiagramCollaborator

__all__ = [
    "Diagram",
    "Clase",
    "Relacion",
    "Atributo",
    "Metodo",
    "User",
    "DiagramCollaborator",
]
