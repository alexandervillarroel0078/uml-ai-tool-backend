# app/services/ia_editor.py
import json, os
from app.services.servicio_analisis import client

def editar_diagrama_con_ia(diagram_data: dict, prompt_usuario: str):
    """
    Envía el diagrama actual + prompt textual a GPT-4o
    y devuelve un nuevo JSON UML modificado.
    """
    prompt_ia = f"""
    Eres un asistente experto en UML y tu tarea es modificar diagramas en formato JSON.
    El JSON debe seguir exactamente esta estructura para que un sistema pueda importarlo a base de datos:

    {{
      "diagram": {{
        "title": "string",
        "classes": [
          {{
            "name": "string",
            "attributes": [
              {{"name": "string", "type": "string", "requerido": bool, "es_primaria": bool}}
            ],
            "methods": [
              {{"name": "string", "tipo_retorno": "string"}}
            ]
          }}
        ],
        "relations": [
          {{
            "from": "string (nombre clase origen)",
            "to": "string (nombre clase destino)",
            "type": "ASSOCIATION | AGGREGATION | COMPOSITION | INHERITANCE | DEPENDENCY",
            "mult_origen_min": int,
            "mult_origen_max": int | null,
            "mult_destino_min": int,
            "mult_destino_max": int | null
          }}
        ]
      }}
    }}

    Mantén la misma estructura y el mismo formato.
    No agregues explicaciones, solo devuelve el JSON final.

    Instrucción del usuario:
    {prompt_usuario}

    Diagrama actual:
    {json.dumps(diagram_data, ensure_ascii=False, indent=2)}
    """

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "Eres un experto en UML y edición estructurada de diagramas JSON."},
            {"role": "user", "content": prompt_ia},
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    return json.loads(content)
