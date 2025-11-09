"""
mapeador_tipos.py
Convierte los tipos del diagrama UML a sus equivalentes en Java.
Ejemplo: "string" → "String", "int" → "Integer".
"""

def mapear_tipo(tipo: str) -> str:
    mapa = {
        "int": "Integer",
        "long": "Long",
        "string": "String",
        "float": "Float",
        "double": "Double",
        "boolean": "Boolean",
        "date": "LocalDate",
        "datetime": "LocalDateTime"
    }
    return mapa.get(tipo.lower(), "String")
