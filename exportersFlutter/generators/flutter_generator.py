import os
import sys
import json
from jinja2 import Environment, FileSystemLoader

# ============================================================
# 🔧 CONFIGURACIÓN DE RUTAS
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
if not os.path.exists(os.path.join(PROJECT_ROOT, "exporters")):
    PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../../"))

sys.path.append(os.path.join(PROJECT_ROOT, "exportersFlutter"))

from generators.json_to_flutter_model import generate_model
from generators.json_to_flutter_service import generate_service
from generators.json_to_flutter_ui import generate_ui
from generators.project_builder_flutter import create_project_structure, generate_base_files

TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "exportersFlutter", "templates")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "exportersFlutter", "APPGENERADA", "flutter_app")

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# ============================================================
# 🧩 FUNCIÓN PRINCIPAL
# ============================================================

def generate_from_json(json_path: str):
    """Lee un archivo JSON UML y genera el frontend Flutter completo."""
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"No se encontró el archivo JSON en: {json_path}")

    print(f"📂 Leyendo JSON desde: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    diagram = data["diagram"]
    print(f"🧩 Generando frontend Flutter para: {diagram['title']}")

    # 1️⃣ Crear estructura base
    create_project_structure(OUTPUT_DIR)

    # 2️⃣ Generar archivos base (main.dart, routes.dart, pubspec.yaml, README.md)
    generate_base_files(OUTPUT_DIR, env, diagram)

    # generar login automáticamente
    login_template = env.get_template("login_screen.dart.j2")
    login_path = os.path.join(OUTPUT_DIR, "lib", "screens", "login_screen.dart")
    with open(login_path, "w", encoding="utf-8") as f:
        f.write(login_template.render(diagram=diagram))
    print("🔐 Pantalla de login generada automáticamente.")

    # generar home automáticamente
    home_template = env.get_template("home_screen.dart.j2")
    home_path = os.path.join(OUTPUT_DIR, "lib", "screens", "home_screen.dart")
    with open(home_path, "w", encoding="utf-8") as f:
        f.write(home_template.render(diagram=diagram))
    print("🏠 Pantalla de inicio (Home) generada automáticamente.")


    # 3️⃣ Generar modelos Dart
    for c in diagram["classes"]:
        generate_model(c, OUTPUT_DIR, env)

    # 4️⃣ Generar servicio API
    generate_service(diagram, OUTPUT_DIR, env)

    # # 5️⃣ Generar pantallas UI (List y Detail)
    # relations_globales = diagram.get("relations", [])

    # for c in diagram["classes"]:
    #     # 🔗 Filtrar relaciones donde la clase actual sea el "from"
    #     relaciones_clase = []
    #     for r in relations_globales:
    #         if r["from"] == c["name"]:
    #             # Solo tomamos las relaciones relevantes
    #             relaciones_clase.append({
    #                 "tipo": (
    #                     "ManyToOne" if r["type"] in ["ASSOCIATION", "COMPOSITION", "AGGREGATION"]
    #                     and r.get("to_max") == 1 else r["type"]
    #                 ),
    #                 "origen": r["from"],
    #                 "destino": r["to"]
    #             })

    #     # 👇 Insertamos las relaciones dentro del diccionario de clase
    #     c["relations"] = relaciones_clase

    #     # 🧩 Generar UI
    #     generate_ui(c, OUTPUT_DIR, env)
    # 5️⃣ Generar pantallas UI (List y Detail)
    relations_globales = diagram.get("relations", [])

    for c in diagram["classes"]:
        relaciones_clase = []

        for r in relations_globales:
            tipo = r["type"].upper()

            # 🧹 Ignorar relaciones que no generan campos en el formulario
            if tipo in ["INHERITANCE", "DEPENDENCY"]:
                continue

            # ✅ Caso 1: la clase es el origen (from)
            if r["from"] == c["name"]:
                if tipo in ["ASSOCIATION", "AGGREGATION", "COMPOSITION"]:
                    relaciones_clase.append({
                        "tipo": "ManyToOne" if r.get("to_max") == 1 else "OneToMany",
                        "origen": r["from"],
                        "destino": r["to"]
                    })

            # ✅ Caso 2: la clase es el destino (to)
            elif r["to"] == c["name"]:
                if tipo in ["ASSOCIATION", "AGGREGATION", "COMPOSITION"]:
                    relaciones_clase.append({
                        "tipo": "ManyToOne" if r.get("from_max") == 1 else "OneToMany",
                        "origen": r["to"],
                        "destino": r["from"]
                    })

        # 🔗 Guardar relaciones detectadas
        c["relations"] = relaciones_clase

        # 🧩 Generar UI (List y Detail)
        generate_ui(c, OUTPUT_DIR, env)


    print(f"\n✅ Proyecto Flutter generado correctamente en:\n   {OUTPUT_DIR}")

# ============================================================
# 🚀 EJECUCIÓN DIRECTA
# ============================================================

if __name__ == "__main__":
    EXPORTERS_JSON_DIR = None
    for possible_dir in ["exporters/json", "exporters copy/json"]:
        path = os.path.join(PROJECT_ROOT, possible_dir)
        if os.path.exists(path):
            EXPORTERS_JSON_DIR = path
            break

    if not EXPORTERS_JSON_DIR:
        print("⚠️ No se encontró ni 'exporters/json' ni 'exporters copy/json'")
        sys.exit(1)

    json_files = [
        f for f in os.listdir(EXPORTERS_JSON_DIR)
        if f.startswith("diagram_") and f.endswith(".json")
    ]
    if not json_files:
        print(f"⚠️ No se encontró ningún archivo JSON UML en {EXPORTERS_JSON_DIR}")
        sys.exit(1)

    json_files.sort(
        key=lambda f: os.path.getmtime(os.path.join(EXPORTERS_JSON_DIR, f)),
        reverse=True
    )
    latest_json = json_files[0]
    json_path = os.path.join(EXPORTERS_JSON_DIR, latest_json)

    print(f"📄 Usando JSON UML más reciente: {latest_json}")
    generate_from_json(json_path)
