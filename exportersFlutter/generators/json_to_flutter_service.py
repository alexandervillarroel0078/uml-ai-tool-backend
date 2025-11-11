import os
from jinja2 import Environment

def generate_service(diagram: dict, output_dir: str, env: Environment):
    """Genera el servicio API base para Flutter."""
    template = env.get_template("api_service.dart.j2")

    code = template.render(
        base_url="http://localhost:8080",  # ✅ Conexión correcta al backend Spring Boot
        entities=[c["name"].lower() for c in diagram["classes"]],
    )

    service_path = os.path.join(output_dir, "lib", "services", "api_service.dart")
    with open(service_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"🌐 Servicio API generado: {service_path}")
