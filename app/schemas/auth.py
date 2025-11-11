# app/schemas/auth.py
from pydantic import BaseModel, Field
from typing import Optional

# ====== INPUTS ======
class SignUpIn(BaseModel):
    """Datos que envía el cliente para registrarse"""
    email: str
    name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=8, max_length=128)


class SignInIn(BaseModel):
    """Datos que envía el cliente para iniciar sesión"""
    email: str
    password: str


# ====== OUTPUTS ======
class UserOut(BaseModel):
    id: int
    email: str
    name: str
    role: str
    active: bool

    model_config = {"from_attributes": True}


class TokensOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None


class LoginResponse(BaseModel):
    tokens: TokensOut
    user: UserOut
