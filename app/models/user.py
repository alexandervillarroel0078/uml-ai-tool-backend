# app/models/user.py
from sqlalchemy.orm import Mapped, mapped_column, relationship   # 👈 aquí agregamos relationship
from sqlalchemy import String, Boolean, DateTime, func, Enum, text
import datetime, enum
from typing import List

from ..db import Base


# =========================
# Enumeración de roles
# =========================
class Role(str, enum.Enum):
    admin = "admin"
    editor = "editor"
    viewer = "viewer"


# =========================
# Modelo User
# =========================
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[Role] = mapped_column(
        Enum(Role, name="user_role"),
        nullable=False,
        server_default=text("'editor'")
    )

    active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # =========================
    # Relaciones
    # =========================

    # Diagramas creados por el usuario (dueño)
    diagrams: Mapped[List["Diagram"]] = relationship(back_populates="owner")

    # Diagramas compartidos con el usuario (colaboraciones)
    shared_diagrams: Mapped[List["DiagramCollaborator"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
