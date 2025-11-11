# #exporters/generators/generador_uml/generador_entidades.py
# """
# generador_entidades.py
# Genera una clase Java completa (atributos + relaciones + getters/setters)
# basada en la definición UML y su mapa de relaciones (JPA).
# """

# from exporters.generators.generador_uml.mapeador_tipos import mapear_tipo
# from exporters.generators.generador_uml.manejador_herencia import detectar_herencia
# from exporters.generators.generador_uml.utilidades import a_camel
# from exporters.generators.relaciones.helpers import render_relations


# def generar_entidad(clase: dict, mapa_relaciones: dict):
#     """
#     Genera el código Java de una entidad (clase JPA) con:
#       - atributos normales
#       - relaciones (usando render_relations)
#       - herencia si aplica
#       - getters y setters
#     """
#     nombre = clase["name"]
#     atributos = clase.get("attributes", [])

#     # 🧬 Detectar si hereda de otra clase
#     padre, anotacion = detectar_herencia(nombre, mapa_relaciones)
#     es_hija = padre is not None

#     # 🆔 Agregar ID si no existe (solo si no es hija)
#     if not any(a["name"].lower() == "id" for a in atributos) and not es_hija:
#         atributos.insert(0, {"name": "id", "type": "long", "required": True})

#     lineas = []
#     lineas.append("package com.test.models;\n")
#     lineas.append("import jakarta.persistence.*;")
#     lineas.append("import java.time.*;")
#     lineas.append("import java.util.*;\n")
#     lineas.append("@Entity")

#     if anotacion:
#         lineas.append(anotacion)

#     hereda = f" extends {padre}" if padre else ""
#     lineas.append(f"public class {nombre}{hereda} {{\n")

#     # 🧱 Atributos básicos
#     for att in atributos:
#         tipo = "Long" if att["name"].lower() == "id" else mapear_tipo(att["type"])
#         if att["name"].lower() == "id":
#             lineas.append("    @Id")
#             lineas.append("    @GeneratedValue(strategy = GenerationType.IDENTITY)")
#         lineas.append(f"    private {tipo} {a_camel(att['name'])};\n")

#     # 🔗 Relaciones (procesadas por builder + handlers)
#     lineas.extend(render_relations(nombre, mapa_relaciones))

#     # ⚙️ Getters y Setters
#     for att in atributos:
#         nombre_attr = a_camel(att["name"])
#         tipo = "Long" if att["name"].lower() == "id" else mapear_tipo(att["type"])
#         metodo = nombre_attr[0].upper() + nombre_attr[1:]
#         lineas.append(f"    public {tipo} get{metodo}() {{ return {nombre_attr}; }}")
#         lineas.append(f"    public void set{metodo}({tipo} {nombre_attr}) {{ this.{nombre_attr} = {nombre_attr}; }}\n")

#     lineas.append("}\n")
#     return "\n".join(lineas)
# exporters/generators/generador_uml/generador_entidades.py
"""
generador_entidades.py
Genera una clase Java completa (atributos + relaciones + getters/setters)
basada en la definición UML y su mapa de relaciones (JPA).
"""

from exporters.generators.generador_uml.mapeador_tipos import mapear_tipo
from exporters.generators.generador_uml.manejador_herencia import detectar_herencia
from exporters.generators.generador_uml.utilidades import a_camel
from exporters.generators.relaciones.helpers import render_relations


def generar_entidad(clase: dict, mapa_relaciones: dict):
    """
    Genera el código Java de una entidad (clase JPA) con:
      - atributos normales
      - relaciones (usando render_relations)
      - herencia si aplica
      - getters y setters
    """
    nombre = clase["name"]
    atributos = clase.get("attributes", [])

    # 🧬 Detectar si hereda de otra clase
    padre, anotacion = detectar_herencia(nombre, mapa_relaciones)
    es_hija = padre is not None

    # 🆔 Agregar ID si no existe (solo si no es hija)
    if not any(a["name"].lower() == "id" for a in atributos) and not es_hija:
        atributos.insert(0, {"name": "id", "type": "long", "required": True})

    lineas = []
    lineas.append("package com.test.models;\n")
    lineas.append("import jakarta.persistence.*;")
    lineas.append("import com.fasterxml.jackson.annotation.JsonIdentityReference;")
    lineas.append("import java.time.*;")
    lineas.append("import java.util.*;\n")
    lineas.append("@Entity")

    if anotacion:
        lineas.append(anotacion)

    hereda = f" extends {padre}" if padre else ""
    lineas.append(f"public class {nombre}{hereda} {{\n")

    # 🧱 Atributos básicos
    for att in atributos:
        tipo = "Long" if att["name"].lower() == "id" else mapear_tipo(att["type"])
        if att["name"].lower() == "id":
            lineas.append("    @Id")
            lineas.append("    @GeneratedValue(strategy = GenerationType.IDENTITY)")
        lineas.append(f"    private {tipo} {a_camel(att['name'])};\n")

    # 🔗 Relaciones (procesadas por builder + handlers)
    relaciones_render = render_relations(nombre, mapa_relaciones)
    for linea in relaciones_render:
        if "@ManyToOne" in linea or "@OneToOne" in linea:
            lineas.append("    @JsonIdentityReference(alwaysAsId = false)")
        lineas.append(linea)

    # ⚙️ Getters y Setters
    for att in atributos:
        nombre_attr = a_camel(att["name"])
        tipo = "Long" if att["name"].lower() == "id" else mapear_tipo(att["type"])
        metodo = nombre_attr[0].upper() + nombre_attr[1:]
        lineas.append(f"    public {tipo} get{metodo}() {{ return {nombre_attr}; }}")
        lineas.append(f"    public void set{metodo}({tipo} {nombre_attr}) {{ this.{nombre_attr} = {nombre_attr}; }}\n")

    lineas.append("}\n")
    return "\n".join(lineas)
