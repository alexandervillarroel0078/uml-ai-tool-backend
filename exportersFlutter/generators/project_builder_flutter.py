import os
from jinja2 import Environment, FileSystemLoader

def create_project_structure(base_dir: str):
    """
    Crea las carpetas base del proyecto Flutter.
    """
    os.makedirs(os.path.join(base_dir, "lib", "models"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "lib", "screens"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "lib", "services"), exist_ok=True)
    print(f"📁 Estructura creada en {base_dir}")


def generate_base_files(base_dir: str, env: Environment, diagram: dict):
    """
    Genera los archivos base de Flutter (main.dart, routes.dart, pubspec.yaml, README.md)
    usando las plantillas .j2
    """
    print("🧱 Generando archivos base de Flutter...")

    templates = {
        "main.dart.j2": os.path.join(base_dir, "lib", "main.dart"),
        "routes.dart.j2": os.path.join(base_dir, "lib", "routes.dart"),
        "pubspec.yaml.j2": os.path.join(base_dir, "pubspec.yaml"),
        "README.md.j2": os.path.join(base_dir, "README.md")
    }

    for template_name, output_path in templates.items():
        template = env.get_template(template_name)
        rendered = template.render(diagram=diagram)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)

        print(f"✅ Generado: {output_path}")
