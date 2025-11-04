# app/schemas/diagram.py
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from .collaborator import DiagramCollaboratorOut


# ====== INPUTS ======
class DiagramCreate(BaseModel):
    title: str


class DiagramUpdate(BaseModel):
    title: Optional[str] = None


# ====== OUTPUTS ======
class DiagramOut(BaseModel):
    id: UUID
    title: str
    owner_id: int
    updated_at: datetime
    collaborators: list[DiagramCollaboratorOut]
    is_owner: bool = None # 👈 Nuevo campo

    model_config = {"from_attributes": True}


class DiagramList(BaseModel):
    items: List[DiagramOut]
    page: int
    limit: int
    total: int
