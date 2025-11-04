# app/models/collaborator.py
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import Base
import uuid
import datetime

class DiagramCollaborator(Base):
    __tablename__ = "diagram_collaborator"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    diagram_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("diagram.id", ondelete="CASCADE"), primary_key=True
    )
    added_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relaciones inversas
    user: Mapped["User"] = relationship(back_populates="shared_diagrams")
    diagram: Mapped["Diagram"] = relationship(back_populates="collaborators")
