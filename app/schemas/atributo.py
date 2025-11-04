# app/schemas/atributo.py
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class AtributoCreate(BaseModel):
    # name: str = Field(alias="nombre")
    # type: str = Field(alias="tipo")
    # required: bool = Field(default=False, alias="requerido")
    # es_primaria: bool = Field(default=False)
    name: str
    type: str
    required: bool = False
    es_primaria: bool = False
    
class AtributoUpdate(BaseModel):
    name: Optional[str] = Field(default=None, alias="nombre")
    type: Optional[str] = Field(default=None, alias="tipo")
    required: Optional[bool] = Field(default=None, alias="requerido")
    es_primaria: Optional[bool] = None

class AtributoOut(BaseModel):
    id: UUID
    name: str = Field(alias="nombre")
    type: str = Field(alias="tipo")
    required: bool = Field(alias="requerido")
    es_primaria: bool

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
