#exporters/generators/generador_uml/principal_generador.py
"""
principal_generador.py
Archivo principal del generador.
Lee el JSON exportado desde el UML y genera las clases Java completas.
"""

import os, json
from exporters.generators.json_to_relations import build_relations
from exporters.generators.generador_uml.generador_entidades import generar_entidad

def generar_desde_json(ruta_json: str, carpeta_salida=None):
    """Lee un archivo UML en JSON y genera las entidades Java completas."""
    if carpeta_salida is None:
        carpeta_salida = os.path.join(os.path.dirname(__file__), "..", "generated", "models")
        os.makedirs(carpeta_salida, exist_ok=True)

    with open(ruta_json, "r", encoding="utf-8") as f:
        datos = json.load(f)

    diagrama = datos["diagram"]
    relaciones = build_relations(ruta_json)

    for clase in diagrama["classes"]:
        codigo = generar_entidad(clase, relaciones)
        archivo = os.path.join(carpeta_salida, f"{clase['name']}.java")
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(codigo)
        print(f"✅ Generada entidad con relaciones: {archivo}")

if __name__ == "__main__":
    generar_desde_json("../json/diagram.json")
