import os

def map_type(t):
    mapping = {
        "String": "String",
        "Integer": "int",
        "Decimal": "double",
        "Date": "DateTime",
        "UUID": "String",
        "Boolean": "bool"
    }
    return mapping.get(t, "String")

def generate_model(class_def, output_dir, env):
    template = env.get_template("model.dart.j2")
    attrs = []
    for a in class_def.get("attributes", []):
        attrs.append({
            "name": a["name"],
            "type": map_type(a["type"])
        })
    code = template.render(class_name=class_def["name"], attributes=attrs)
    file_path = os.path.join(output_dir, "lib", "models", f"{class_def['name'].lower()}.dart")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"🧱 Modelo generado: {file_path}")
