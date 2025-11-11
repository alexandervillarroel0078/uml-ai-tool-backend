import os
from jinja2 import Environment

def generate_ui(class_def: dict, output_dir: str, env: Environment):
    """Genera pantallas List y Detail para cada clase."""
    class_name = class_def["name"]
    attributes = class_def.get("attributes", [])
    relations = class_def.get("relations", [])  # 👈 se añade esta línea

    list_template = env.get_template("screen_list.dart.j2")
    detail_template = env.get_template("screen_detail.dart.j2")

    # 🧩 List Screen
    list_code = list_template.render(
        class_name=class_name,
        attributes=attributes,
        relations=relations  # 👈 también se pasa al template
    )
    list_path = os.path.join(output_dir, "lib", "screens", f"{class_name.lower()}_list_screen.dart")
    with open(list_path, "w", encoding="utf-8") as f:
        f.write(list_code)

    # 🧩 Detail Screen
    detail_code = detail_template.render(
        class_name=class_name,
        attributes=attributes,
        relations=relations  # 👈 importante para generar los Dropdowns
    )
    detail_path = os.path.join(output_dir, "lib", "screens", f"{class_name.lower()}_detail_screen.dart")
    with open(detail_path, "w", encoding="utf-8") as f:
        f.write(detail_code)

    print(f"🖥️ Pantallas generadas: {class_name}_list_screen.dart y {class_name}_detail_screen.dart")
