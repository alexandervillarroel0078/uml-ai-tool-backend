 
import os
import json
import base64
import logging
from pathlib import Path
from datetime import datetime
from openai import OpenAI

# ================================
# 🔧 Configuración general
# ================================
UPLOAD_DIR = Path("app/uploads")
LOGS_DIR = Path("app/logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "analisis_uml.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analizar_imagen_uml(ruta_imagen: str) -> dict:
    """
    🧠 Analiza una imagen UML usando GPT-4o (visión)
    y devuelve un JSON estructurado con clases, atributos, relaciones y posiciones aproximadas.
    """

    nombre_archivo = Path(ruta_imagen).stem
    logging.info(f"📷 Analizando imagen: {nombre_archivo}")

    # Leer imagen en base64
    with open(ruta_imagen, "rb") as img_file:
        imagen_b64 = base64.b64encode(img_file.read()).decode("utf-8")

    # prompt = f"""
    # Eres un experto en ingeniería de software y análisis de diagramas UML de clases.
    # Analiza cuidadosamente la imagen adjunta y genera un JSON válido con esta estructura exacta:

    # {{
    #   "diagram": {{
    #     "title": "{nombre_archivo}",
    #     "classes": [
    #       {{
    #         "name": "NombreClase",
    #         "x": 12,
    #         "y": 6,
    #         "attributes": [
    #           {{"name": "atributo", "type": "String", "required": true, "es_primaria": false}}
    #         ]
    #       }}
    #     ],
    #     "relations": [
    #       {{
    #         "from": "ClaseA",
    #         "to": "ClaseB",
    #         "type": "ASSOCIATION | AGGREGATION | COMPOSITION | INHERITANCE | DEPENDENCY | SELF",
    #         "label": "nombreRelacionOpcional",
    #         "from_min": "1",
    #         "from_max": "*",
    #         "to_min": "0",
    #         "to_max": "1"
    #       }}
    #     ]
    #   }}
    # }}

    # 🔎 Indicaciones:
    # - Detecta todas las clases (rectángulos con nombre en la parte superior).
    # - Extrae los atributos (líneas internas con tipo o nombre).
    # - Si hay métodos, inclúyelos dentro de "methods".
    # - Si una clase se conecta a sí misma, usa type: "SELF".
    # - Calcula coordenadas aproximadas "x" y "y" según su posición visual (de izquierda a derecha, arriba a abajo).
    # - Si no puedes determinar posición exacta, usa x=0, y=0.
    # - Usa los nombres de las clases y relaciones tal como aparecen.
    # - Devuelve **solo JSON válido**, sin texto adicional.
    # """
    prompt = f"""
    Eres un experto en ingeniería de software y análisis de diagramas UML de clases.

    Analiza la imagen adjunta y genera un JSON **válido** con esta estructura exacta:

    {{
      "diagram": {{
        "title": "{nombre_archivo}",
        "classes": [
          {{
            "name": "NombreClase",
            "x": 10,
            "y": 6,
            "attributes": [
              {{"name": "atributo", "type": "String", "required": true, "es_primaria": false}}
            ],
            "methods": [
              {{"name": "metodo", "tipo_retorno": "void"}}
            ]
          }}
        ],
        "relations": [
          {{
            "from": "ClaseA",
            "to": "ClaseB",
            "type": "ASSOCIATION | AGGREGATION | COMPOSITION | INHERITANCE | DEPENDENCY | SELF",
            "label": "nombreRelacionOpcional",
            "from_min": "1",
            "from_max": "*",
            "to_min": "0",
            "to_max": "1"
          }}
        ]
      }}
    }}

    🔎 Instrucciones:
    - La imagen tiene una cuadrícula visible: considera el eje X (0–80) y eje Y (0–50).
    - Usa esa cuadrícula para ubicar cada clase con coordenadas aproximadas (x,y).
    - Si hay varias clases alineadas horizontalmente, distribúyelas en el eje X.
    - Si están una debajo de otra, distribúyelas en el eje Y.
    - Detecta:
      • Nombre de cada clase (parte superior del rectángulo).
      • Atributos (líneas dentro del rectángulo con tipo o nombre).
      • Relaciones (líneas o flechas entre clases).
    - Si hay una clase que se conecta a sí misma, usa "type": "SELF".
    - Si no puedes determinar posición exacta, usa valores aproximados pero dentro del rango.
    - Devuelve SOLO JSON válido.
    """

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        messages=[
            {"role": "system", "content": "Eres un experto en UML y visión por computadora."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt.strip()},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{imagen_b64}"}}
                ]
            }
        ],
        response_format={"type": "json_object"}
    )

    try:
        # ===========================
        # 🧠 Llamada a GPT-4o (visión)
        # ===========================
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            messages=[
                {"role": "system", "content": "Eres un experto en UML y visión por computadora."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt.strip()},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{imagen_b64}"}}
                    ]
                }
            ],
            response_format={"type": "json_object"}
        )

        raw = response.choices[0].message.content
        logging.info(f"📤 Respuesta cruda del modelo: {raw[:400]}...")
        result = json.loads(raw)

        usage = getattr(response, "usage", None)
        tokens = usage.total_tokens if usage else "?"
        logging.info(f"💰 Tokens usados: {tokens} | Modelo: {os.getenv('OPENAI_MODEL', 'gpt-4o')}")

    except Exception as e:
        logging.error(f"⚠️ Error en IA: {e}")
        result = {
            "diagram": {
                "title": f"{nombre_archivo} (Error o no detectado)",
                "classes": [],
                "relations": []
            }
        }

    # Guardar resultado
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    ruta_json = UPLOAD_DIR / f"{nombre_archivo}_uml.json"
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    logging.info(f"✅ Análisis completado y guardado en {ruta_json}")
    return result
