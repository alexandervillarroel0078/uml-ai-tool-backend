# app/services/ia_editor_text.py
import os, json
from app.services.servicio_analisis import client

def procesar_edicion_ia(diagram_data: dict, prompt_usuario: str):
    """
    Envía el JSON actual del diagrama + prompt textual a la IA
    y devuelve un nuevo JSON con las modificaciones.
    """
    prompt_ia = f"""
    Eres un asistente experto en UML.
    Recibirás un diagrama UML en formato JSON y una instrucción del usuario.
    Aplica los cambios pedidos (crear, editar, eliminar clases, atributos o relaciones)
    sin cambiar el formato del JSON.

    Instrucción:
    {prompt_usuario}

    Diagrama actual:
    {json.dumps(diagram_data, ensure_ascii=False, indent=2)}

    Devuelve únicamente el nuevo JSON actualizado, bien formado y coherente.
    """

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        messages=[
            {"role": "system", "content": "Eres un experto en UML y edición estructurada de diagramas."},
            {"role": "user", "content": prompt_ia},
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    return json.loads(content)
