"""
asociacion_handler.py
Gestiona relaciones de tipo ASSOCIATION (1:N, N:1, 1:1, N:N y recursivas).
Evita duplicar tablas intermedias y detecta automáticamente relaciones recursivas.
100% genérico: funciona con cualquier nombre de clase.
"""

from exporters.generators.relaciones.helpers import to_camel

def handle_association(rel, relations_map):
    src = rel["from"]       # Clase origen
    dst = rel["to"]         # Clase destino
    from_max = rel.get("from_max")
    to_max = rel.get("to_max")

    # Evitar duplicados (bidireccionales)
    if dst in relations_map.get(src, {}):
        return

    relations_map.setdefault(src, {})
    relations_map.setdefault(dst, {})

    # 🌀 CASO 1: Asociación recursiva (la clase se relaciona consigo misma)
    if src == dst:
        # 🔁 Caso N:N recursivo (Ej: Curso ↔ Curso, Empleado ↔ Empleado)
        if (from_max in (None, "*")) and (to_max in (None, "*")):
            join_name = f"{to_camel(src)}_relacion"
            relacionados_name = f"{to_camel(src)}Relacionados"
            relacionados_con_name = f"{to_camel(src)}RelacionadosCon"

            # ✅ Ambos lados dentro de la misma clase (recursiva)
            relations_map[src][f"{src}_relacionados"] = {
                "type": "ManyToMany",
                "annotation": (
                    "@ManyToMany\n"
                    f"    @JoinTable(name = \"{join_name}\", "
                    f"joinColumns = @JoinColumn(name = \"{to_camel(src)}_id\"), "
                    f"inverseJoinColumns = @JoinColumn(name = \"relacionado_id\"))"
                ),
                "label": relacionados_name
            }
            relations_map[src][f"{src}_relacionados_con"] = {
                "type": "ManyToMany",
                "annotation": f"@ManyToMany(mappedBy = \"{relacionados_name}\")",
                "label": relacionados_con_name
            }
            return


        # 👔 Caso 1:N recursivo (Ej: Categoria ↔ Categoria)
        if ((from_max in (None, "*") and to_max in (None, 1))
            or (from_max in (None, 1) and to_max in (None, "*"))):
            padre_name = f"{to_camel(src)}Padre"
            hijos_name = f"{to_camel(src)}Hijos"

            # ✅ Ambos campos viven dentro de la misma clase (recursiva)
            relations_map[src][f"{src}_padre"] = {
                "type": "ManyToOne",
                "annotation": "@ManyToOne",
                "joinColumn": f"{to_camel(src)}_padre_id",
                "label": padre_name
            }
            relations_map[src][f"{src}_hijos"] = {
                "type": "OneToMany",
                "annotation": f"@OneToMany(mappedBy = \"{padre_name}\")",
                "label": hijos_name
            }
            return


        # 🧩 Caso 1:1 recursivo
        if (from_max == 1) and (to_max == 1):
            rel_name = f"{to_camel(dst)}Relacion"
            inv_name = f"{to_camel(dst)}Inverso"

            relations_map[src][dst] = {
                "type": "OneToOne",
                "annotation": "@OneToOne",
                "joinColumn": f"{to_camel(dst)}_relacion_id",
                "label": rel_name
            }
            relations_map[dst][src] = {
                "type": "OneToOne",
                "annotation": f"@OneToOne(mappedBy = \"{rel_name}\")",
                "label": inv_name
            }
            return

    # 🧩 CASO 2: Asociación normal entre distintas clases
    # --- N:N ---
    if (from_max in (None, "*")) and (to_max in (None, "*")):
        join_name = f"{to_camel(src)}_{to_camel(dst)}"
        var_src = f"{to_camel(dst)}s"
        var_dst = f"{to_camel(src)}s"

        relations_map[src][dst] = {
            "type": "ManyToMany",
            "annotation": (
                "@ManyToMany\n"
                f"    @JoinTable(name = \"{join_name}\", "
                f"joinColumns = @JoinColumn(name = \"{to_camel(src)}_id\"), "
                f"inverseJoinColumns = @JoinColumn(name = \"{to_camel(dst)}_id\"))"
            ),
            "label": var_src
        }
        relations_map[dst][src] = {
            "type": "ManyToMany",
            "annotation": f"@ManyToMany(mappedBy = \"{var_src}\")",
            "label": var_dst
        }
        return

    # --- 1:N ---
    if from_max == 1 and (to_max in (None, "*")):
        one_name = f"{to_camel(dst)}s"
        many_name = to_camel(src)

        relations_map[src][dst] = {
            "type": "OneToMany",
            "annotation": f"@OneToMany(mappedBy = \"{many_name}\")",
            "label": one_name
        }
        relations_map[dst][src] = {
            "type": "ManyToOne",
            "annotation": "@ManyToOne",
            "joinColumn": f"{to_camel(src)}_id",
            "label": many_name
        }
        return

    # --- N:1 ---
    if (from_max in (None, "*")) and to_max == 1:
        one_name = f"{to_camel(src)}s"
        many_name = to_camel(dst)

        relations_map[src][dst] = {
            "type": "ManyToOne",
            "annotation": "@ManyToOne",
            "joinColumn": f"{to_camel(dst)}_id",
            "label": many_name
        }
        relations_map[dst][src] = {
            "type": "OneToMany",
            "annotation": f"@OneToMany(mappedBy = \"{many_name}\")",
            "label": one_name
        }
        return

    # --- 1:1 ---
    if from_max == 1 and to_max == 1:
        rel_name = to_camel(dst)

        relations_map[src][dst] = {
            "type": "OneToOne",
            "annotation": "@OneToOne",
            "joinColumn": f"{to_camel(dst)}_id",
            "label": rel_name
        }
        relations_map[dst][src] = {
            "type": "OneToOne",
            "annotation": f"@OneToOne(mappedBy = \"{rel_name}\")",
            "label": to_camel(src)
        }
