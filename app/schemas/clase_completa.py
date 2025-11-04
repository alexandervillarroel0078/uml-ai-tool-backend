# # # # app/schemas/clase_completa.py
# # # from typing import List, Optional, Union, Literal
# # # from uuid import UUID
# # # from pydantic import BaseModel, Field

# # # RelationType = Literal["ASSOCIATION", "AGGREGATION", "COMPOSITION", "INHERITANCE", "DEPENDENCY"]
# # # Anchor = Literal["left", "right", "top", "bottom"]

# # # class AtributoOut(BaseModel):
# # #     id: UUID
# # #     name: str = Field(alias="nombre")
# # #     type: str = Field(alias="tipo")
# # #     required: bool = Field(alias="requerido")

# # #     model_config = {
# # #         "from_attributes": True,
# # #         "populate_by_name": True,
# # #     }

# # # class MetodoOut(BaseModel):
# # #     id: UUID
# # #     name: str = Field(alias="nombre")
# # #     return_type: str = Field(alias="tipo_retorno")

# # #     model_config = {
# # #         "from_attributes": True,
# # #         "populate_by_name": True,
# # #     }

# # # class ClaseCompletaOut(BaseModel):
# # #     id: UUID
# # #     name: str = Field(alias="nombre")

# # #     # layout
# # #     x_grid: int
# # #     y_grid: int
# # #     w_grid: int
# # #     h_grid: int
# # #     z_index: int

# # #     # hijos
# # #     atributos: List[AtributoOut] = []
# # #     metodos: List[MetodoOut] = []

# # #     model_config = {
# # #         "from_attributes": True,
# # #         "populate_by_name": True,
# # #     }


# # # #schemas exclusivos para recursivos
# # # class ClaseCompletaOutLight(BaseModel):
# # #     id: UUID
# # #     nombre: str
# # #     x_grid: int
# # #     y_grid: int
# # #     w_grid: int
# # #     h_grid: int
# # #     z_index: int

# # #     atributos: list[AtributoOut]
# # #     metodos: list[MetodoOut]

# # #     model_config = {
# # #         "from_attributes": True,
# # #         "populate_by_name": True,
# # #     }

# # # class RelacionOutExpanded(BaseModel):
# # #     id: UUID
# # #     type: RelationType = Field(alias="tipo")
# # #     label: Optional[str] = Field(default=None, alias="etiqueta")

# # #     src_anchor: Anchor
# # #     dst_anchor: Anchor
# # #     src_offset: int
# # #     dst_offset: int
# # #     src_lane: int
# # #     dst_lane: int

# # #     src_mult_min: Optional[int] = Field(alias="mult_origen_min")
# # #     src_mult_max: Optional[int] = Field(alias="mult_origen_max")
# # #     dst_mult_min: Optional[int] = Field(alias="mult_destino_min")
# # #     dst_mult_max: Optional[int] = Field(alias="mult_destino_max")

# # #     # 🚀 En vez de solo IDs/nombres, incluyes las clases completas
# # #     origen: ClaseCompletaOutLight
# # #     destino: ClaseCompletaOutLight

# # #     model_config = {
# # #         "from_attributes": True,
# # #         "populate_by_name": True,
# # #     }
# # # app/schemas/clase_completa.py
# # from typing import List, Optional, Literal
# # from uuid import UUID
# # from pydantic import BaseModel, Field

# # # ==========================================================
# # # 🔹 Tipos literales usados en relaciones
# # # ==========================================================
# # RelationType = Literal["ASSOCIATION", "AGGREGATION", "COMPOSITION", "INHERITANCE", "DEPENDENCY"]
# # Anchor = Literal["left", "right", "top", "bottom"]

# # # ==========================================================
# # # 🔹 Atributo (incluye campo es_primaria)
# # # ==========================================================
# # class AtributoOut(BaseModel):
# #     id: UUID
# #     name: str = Field(alias="nombre")
# #     type: str = Field(alias="tipo")
# #     required: bool = Field(alias="requerido")
# #     es_primaria: bool = Field(alias="es_primaria", default=False)  # ✅ ahora visible en JSON

# #     model_config = {
# #         "from_attributes": True,
# #         "populate_by_name": True,
# #     }

# # # ==========================================================
# # # 🔹 Método
# # # ==========================================================
# # class MetodoOut(BaseModel):
# #     id: UUID
# #     name: str = Field(alias="nombre")
# #     return_type: str = Field(alias="tipo_retorno")

# #     model_config = {
# #         "from_attributes": True,
# #         "populate_by_name": True,
# #     }

# # # ==========================================================
# # # 🔹 Clase completa (con atributos + métodos)
# # # ==========================================================
# # class ClaseCompletaOut(BaseModel):
# #     id: UUID
# #     name: str = Field(alias="nombre")

# #     # layout
# #     x_grid: int
# #     y_grid: int
# #     w_grid: int
# #     h_grid: int
# #     z_index: int

# #     # hijos
# #     atributos: List[AtributoOut] = []   # ✅ usa AtributoOut completo
# #     metodos: List[MetodoOut] = []

# #     model_config = {
# #         "from_attributes": True,
# #         "populate_by_name": True,
# #     }

# # # ==========================================================
# # # 🔹 Versión light (usada en relaciones recursivas)
# # # ==========================================================
# # class ClaseCompletaOutLight(BaseModel):
# #     id: UUID
# #     nombre: str
# #     x_grid: int
# #     y_grid: int
# #     w_grid: int
# #     h_grid: int
# #     z_index: int

# #     atributos: List[AtributoOut] = []  # ✅ también aquí
# #     metodos: List[MetodoOut] = []

# #     model_config = {
# #         "from_attributes": True,
# #         "populate_by_name": True,
# #     }

# # # ==========================================================
# # # 🔹 Relación expandida (usada en diagramas)
# # # ==========================================================
# # class RelacionOutExpanded(BaseModel):
# #     id: UUID
# #     type: RelationType = Field(alias="tipo")
# #     label: Optional[str] = Field(default=None, alias="etiqueta")

# #     src_anchor: Anchor
# #     dst_anchor: Anchor
# #     src_offset: int
# #     dst_offset: int
# #     src_lane: int
# #     dst_lane: int

# #     src_mult_min: Optional[int] = Field(alias="mult_origen_min")
# #     src_mult_max: Optional[int] = Field(alias="mult_origen_max")
# #     dst_mult_min: Optional[int] = Field(alias="mult_destino_min")
# #     dst_mult_max: Optional[int] = Field(alias="mult_destino_max")

# #     # 🚀 Incluye clases recursivas (light)
# #     origen: ClaseCompletaOutLight
# #     destino: ClaseCompletaOutLight

# #     model_config = {
# #         "from_attributes": True,
# #         "populate_by_name": True,
# #     }
# # app/schemas/clase_completa.py
# from typing import List, Optional, Literal
# from uuid import UUID
# from pydantic import BaseModel, Field
# from app.schemas.atributo import AtributoOut

# RelationType = Literal["ASSOCIATION", "AGGREGATION", "COMPOSITION", "INHERITANCE", "DEPENDENCY"]
# Anchor = Literal["left", "right", "top", "bottom"]


# class AtributoOut(BaseModel):
#     id: UUID
#     name: str = Field(alias="nombre")     # 👈 devolverá "name"
#     type: str = Field(alias="tipo")       # 👈 devolverá "type"
#     required: bool = Field(alias="requerido")
#     es_primaria: bool                     # 👈 no cambia

#     model_config = {
#         "from_attributes": True,
#         "populate_by_name": True,
#     }


# class MetodoOut(BaseModel):
#     id: UUID
#     name: str = Field(alias="nombre")
#     return_type: str = Field(alias="tipo_retorno")

#     model_config = {
#         "from_attributes": True,
#         "populate_by_name": True,
#     }


# class ClaseCompletaOut(BaseModel):
#     id: UUID
#     name: str = Field(alias="nombre")  # 👈 mantiene alias para compatibilidad frontend

#     x_grid: int
#     y_grid: int
#     w_grid: int
#     h_grid: int
#     z_index: int

#     atributos: List[AtributoOut] = []
#     metodos: List[MetodoOut] = []

#     model_config = {
#         "from_attributes": True,
#         "populate_by_name": True,
#     }


# class ClaseCompletaOutLight(BaseModel):
#     id: UUID
#     name: str = Field(alias="nombre")  # 👈 igual aquí

#     x_grid: int
#     y_grid: int
#     w_grid: int
#     h_grid: int
#     z_index: int

#     atributos: list[AtributoOut]
#     metodos: list[MetodoOut]

#     model_config = {
#         "from_attributes": True,
#         "populate_by_name": True,
#     }


# class RelacionOutExpanded(BaseModel):
#     id: UUID
#     type: RelationType = Field(alias="tipo")
#     label: Optional[str] = Field(default=None, alias="etiqueta")

#     src_anchor: Anchor
#     dst_anchor: Anchor
#     src_offset: int
#     dst_offset: int
#     src_lane: int
#     dst_lane: int

#     src_mult_min: Optional[int] = Field(alias="mult_origen_min")
#     src_mult_max: Optional[int] = Field(alias="mult_origen_max")
#     dst_mult_min: Optional[int] = Field(alias="mult_destino_min")
#     dst_mult_max: Optional[int] = Field(alias="mult_destino_max")

#     origen: ClaseCompletaOutLight
#     destino: ClaseCompletaOutLight

#     model_config = {
#         "from_attributes": True,
#         "populate_by_name": True,
#     }
# ✅ app/schemas/clase_completa.py
from typing import List, Optional, Literal
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.atributo import AtributoOut  # 👈 Usa el modelo correcto

# === ENUMS / LITERALES ===
RelationType = Literal[
    "ASSOCIATION", "AGGREGATION", "COMPOSITION", "INHERITANCE", "DEPENDENCY"
]
Anchor = Literal["left", "right", "top", "bottom"]


# === MÉTODOS ===
class MetodoOut(BaseModel):
    id: UUID
    name: str = Field(alias="nombre")
    return_type: str = Field(alias="tipo_retorno")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# === CLASE COMPLETA ===
class ClaseCompletaOut(BaseModel):
    id: UUID
    name: str = Field(alias="nombre")

    x_grid: int
    y_grid: int
    w_grid: int
    h_grid: int
    z_index: int

    atributos: List[AtributoOut] = []
    metodos: List[MetodoOut] = []

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# === CLASE LIGHT (para relaciones) ===
class ClaseCompletaOutLight(BaseModel):
    id: UUID
    name: str = Field(alias="nombre")

    x_grid: int
    y_grid: int
    w_grid: int
    h_grid: int
    z_index: int

    atributos: list[AtributoOut] = []
    metodos: list[MetodoOut] = []

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# === RELACIONES EXPANDIDAS ===
class RelacionOutExpanded(BaseModel):
    id: UUID
    type: RelationType = Field(alias="tipo")
    label: Optional[str] = Field(default=None, alias="etiqueta")

    src_anchor: Anchor
    dst_anchor: Anchor
    src_offset: int
    dst_offset: int
    src_lane: int
    dst_lane: int

    src_mult_min: Optional[int] = Field(alias="mult_origen_min")
    src_mult_max: Optional[int] = Field(alias="mult_origen_max")
    dst_mult_min: Optional[int] = Field(alias="mult_destino_min")
    dst_mult_max: Optional[int] = Field(alias="mult_destino_max")

    origen: ClaseCompletaOutLight
    destino: ClaseCompletaOutLight

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
