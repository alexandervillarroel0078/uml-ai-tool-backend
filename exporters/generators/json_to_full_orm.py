
#exporters/generators/json_to_full_orm.py
"""
json_to_full_orm.py
Archivo puente (compatibilidad con versiones anteriores).

👉 Redirige al nuevo módulo modularizado:
   generators/generador_uml/principal_generador.py
"""

import os
from exporters.generators.generador_uml.principal_generador import generar_desde_json

def generate_from_json(json_path: str, output_dir=None):
    """Mantiene compatibilidad con los scripts antiguos."""
    generar_desde_json(json_path, output_dir)

if __name__ == "__main__":
    ruta = os.path.join(os.path.dirname(__file__), "../json/diagram.json")
    generate_from_json(ruta)
