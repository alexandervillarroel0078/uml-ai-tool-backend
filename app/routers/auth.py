
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.db import get_db
# from app.schemas.auth import SignInIn, TokensOut
# from app.models.user import User
# from app.core.security import verify_password, create_access_token
# from app.core.security import get_current_user
# from app.schemas.auth import UserOut

# router = APIRouter(prefix="/auth", tags=["auth"])

# # POST
# # http://localhost:8000/auth/sign-in
# # {
# #   "email": "admin@example.com",
# #   "password": "changeme123"
# # }

# @router.post("/sign-in", response_model=TokensOut)
# def sign_in(body: SignInIn, db: Session = Depends(get_db)):
#     email = body.email.lower().strip()
#     user = db.query(User).filter(User.email == email).one_or_none()
#     if not user or not verify_password(body.password, user.password_hash):
#         raise HTTPException(status_code=400, detail="Credenciales inválidas")
#     token = create_access_token(sub=email)
#     return TokensOut(access_token=token)


# @router.get("/me", response_model=UserOut)
# def get_me(
#     me: User = Depends(get_current_user),
# ):
#     return me
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.auth import SignInIn, TokensOut, UserOut
from app.models.user import User
from app.core.security import verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])
log = logging.getLogger("app.routers.auth")


# 🔹 Inicio de sesión
@router.post("/sign-in", response_model=TokensOut)
def sign_in(body: SignInIn, db: Session = Depends(get_db)):
    email = body.email.lower().strip()
    log.info(f"🔐 Intento de inicio de sesión -> email={email}")

    user = db.query(User).filter(User.email == email).one_or_none()
    if not user:
        log.warning(f"❌ Usuario no encontrado -> email={email}")
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    if not verify_password(body.password, user.password_hash):
        log.warning(f"⚠️ Contraseña incorrecta -> user_id={user.id}, email={email}")
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    token = create_access_token(sub=email)
    log.info(f"✅ Sesión iniciada -> user_id={user.id}, email={email}, role={user.role}")
    return TokensOut(access_token=token)


# 🔹 Obtener usuario autenticado
@router.get("/me", response_model=UserOut)
def get_me(me: User = Depends(get_current_user)):
    log.info(f"🙋‍♂️ Usuario autenticado -> id={me.id}, email={me.email}")

    # Evitar None para no romper el esquema UserOut
    safe_user = UserOut(
        id=me.id,
        email=me.email or "",
        name=me.name or "Sin nombre",
        role=me.role or "editor",
        active=bool(me.active),
    )

    log.debug(f"📤 Retornando datos de usuario -> {safe_user}")
    return safe_user
