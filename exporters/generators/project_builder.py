
# exporters/generators/project_builder.py
import os
import json
from exporters.generators.json_to_full_orm import generate_from_json
from exporters.generators.model_to_repository import generate_repositories
from exporters.generators.repository_to_service import generate_services
from exporters.generators.service_to_controller import generate_controllers
from exporters.generators.model_to_dto import generate_dtos
from exporters.generators.postman_generator import generate_postman
# exporters/generators/project_builder.py
 
from exporters.generators.json_to_full_orm import generate_from_json

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

def render_template(template_path, context):
    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read().lstrip()
    for key, value in context.items():
        content = content.replace("{{ " + key + " }}", value)
    return content


def build_project(json_path: str, output_dir: str):
    src_main = os.path.join(output_dir, "src", "main", "java", "com", "test")
    src_models = os.path.join(src_main, "models")
    src_repositories = os.path.join(src_main, "repositories")
    src_services = os.path.join(src_main, "services")
    src_controllers = os.path.join(src_main, "controllers")
    src_dtos = os.path.join(src_main, "dtos")
    resources = os.path.join(output_dir, "src", "main", "resources")

    os.makedirs(src_main, exist_ok=True)
    os.makedirs(src_models, exist_ok=True)
    os.makedirs(src_repositories, exist_ok=True)
    os.makedirs(src_services, exist_ok=True)
    os.makedirs(src_controllers, exist_ok=True)
    os.makedirs(src_dtos, exist_ok=True)
    os.makedirs(resources, exist_ok=True)

    # 1) Generar modelos
    generate_from_json(json_path, src_models)

    # 2) Repositorios
    generate_repositories(json_path, src_repositories, TEMPLATES_DIR)

    # 3) Servicios
    generate_services(json_path, src_services, TEMPLATES_DIR)

    # 4) Controladores
    generate_controllers(json_path, src_controllers, TEMPLATES_DIR)

    # 5) DTOs
    generate_dtos(json_path, src_dtos, TEMPLATES_DIR)

    # 6) Postman
    generate_postman(json_path, output_dir)

    # 7) Archivos fijos (HealthController, pom.xml, application.properties, etc.)
    health_content = render_template(
        os.path.join(TEMPLATES_DIR, "health_controller.java.j2"),
        {"groupId": "com.test"}
    )
    with open(os.path.join(src_controllers, "HealthController.java"), "w", encoding="utf-8") as f:
        f.write(health_content)

    pom_content = render_template(
        os.path.join(TEMPLATES_DIR, "pom.xml.j2"),
        {"groupId": "com.test", "artifactId": "demo"}
    )
    with open(os.path.join(output_dir, "pom.xml"), "w", encoding="utf-8") as f:
        f.write(pom_content)

    props_content = render_template(
        os.path.join(TEMPLATES_DIR, "application.properties.j2"),
        {"db_name": "testdb", "db_user": "postgres", "db_pass": "1234"}
    )
    with open(os.path.join(resources, "application.properties"), "w", encoding="utf-8") as f:
        f.write(props_content)

    main_class_content = render_template(
        os.path.join(TEMPLATES_DIR, "main.java.j2"),
        {"groupId": "com.test", "artifactId": "demo"}
    )
    with open(os.path.join(src_main, "DemoApplication.java"), "w", encoding="utf-8") as f:
        f.write(main_class_content)
    
    
    # 8) Módulo de autenticación (JWT) si existen Usuario y Rol
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ✅ Detectar estructura del JSON
    if isinstance(data, dict):
        if "diagram" in data and "classes" in data["diagram"]:
            classes = data["diagram"]["classes"]
        elif "classes" in data:
            classes = data["classes"]
        else:
            classes = []
    elif isinstance(data, list):
        classes = [c for c in data if "name" in c]
    else:
        classes = []

    # ✅ Buscar las clases Usuario y Rol
    if any(c.get("name", "").lower() == "usuario" for c in classes) and \
       any(c.get("name", "").lower() == "rol" for c in classes):
        print("🧩 Generando módulo de autenticación (JWT)...")

        # Crear carpeta security
        src_security = os.path.join(src_main, "security")
        os.makedirs(src_security, exist_ok=True)

        # === AuthController ===
        auth_controller_content = render_template(
            os.path.join(TEMPLATES_DIR, "auth_controller.java.j2"),
            {"package": "com.test"}
        )
        with open(os.path.join(src_controllers, "AuthController.java"), "w", encoding="utf-8") as f:
            f.write(auth_controller_content)

        # === AuthRequest ===
        auth_request_content = render_template(
            os.path.join(TEMPLATES_DIR, "auth_request.java.j2"),
            {"package": "com.test"}
        )
        with open(os.path.join(src_dtos, "AuthRequest.java"), "w", encoding="utf-8") as f:
            f.write(auth_request_content)

        # === AuthResponse ===
        auth_response_content = render_template(
            os.path.join(TEMPLATES_DIR, "auth_response.java.j2"),
            {"package": "com.test"}
        )
        with open(os.path.join(src_dtos, "AuthResponse.java"), "w", encoding="utf-8") as f:
            f.write(auth_response_content)

        # === JwtService ===
        jwt_service_content = render_template(
            os.path.join(TEMPLATES_DIR, "jwt_service.java.j2"),
            {"package": "com.test"}
        )
        with open(os.path.join(src_security, "JwtService.java"), "w", encoding="utf-8") as f:
            f.write(jwt_service_content)

        # === SecurityConfig ===
        security_config_content = render_template(
            os.path.join(TEMPLATES_DIR, "security_config.java.j2"),
            {"package": "com.test"}
        )
        with open(os.path.join(src_security, "SecurityConfig.java"), "w", encoding="utf-8") as f:
            f.write(security_config_content)

        # === Añadir dependencias JWT al pom.xml
        pom_file = os.path.join(output_dir, "pom.xml")
        with open(pom_file, "r", encoding="utf-8") as f:
            pom_data = f.read()

        if "<artifactId>jjwt-api</artifactId>" not in pom_data:
            jwt_deps = """
        <!-- JWT (Json Web Token) -->
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-api</artifactId>
            <version>0.11.5</version>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-impl</artifactId>
            <version>0.11.5</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-jackson</artifactId>
            <version>0.11.5</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
            """.strip()

            pom_data = pom_data.replace("</dependencies>", f"{jwt_deps}\n    </dependencies>")

            with open(pom_file, "w", encoding="utf-8") as f:
                f.write(pom_data)

        print("🔒 Autenticación generada correctamente.")

    print(f"✅ Proyecto generado en: {output_dir}")