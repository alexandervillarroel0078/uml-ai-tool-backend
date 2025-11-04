# app/schemas/collaborator.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class DiagramCollaboratorBase(BaseModel):
    user_id: int
    diagram_id: UUID

class DiagramCollaboratorCreate(DiagramCollaboratorBase):
    pass

class DiagramCollaboratorOut(DiagramCollaboratorBase):
    added_at: datetime

    class Config:
        orm_mode = True
