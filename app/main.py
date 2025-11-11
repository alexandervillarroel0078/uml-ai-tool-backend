# backend/app/main.py
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from dotenv import load_dotenv

load_dotenv()
print("🔑 OPENAI_API_KEY cargada:", os.getenv("OPENAI_API_KEY")[:10], "...")  # ✅ para verificar


from app.core.config import ALLOWED_ORIGINS, settings
from app.routers import auth as auth_router
from app.routers import diagramas, classes, atributos, metodo, relacion, realtime 
from app.routers import classes as classes_router
from app.routers import export 
from app.routers import imagen_uml
from app.routers import ia_edicion
# ===================================
# 🔹 Configuración de logging global
# ===================================
logging.basicConfig(
    level=logging.INFO,  # Cambiá a DEBUG si querés más detalle
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


app = FastAPI(title="UML AI Tool API")
print("🚀 ALLOWED_ORIGINS:", ALLOWED_ORIGINS)
cors_origins = ["*"] if settings.DEBUG else ALLOWED_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/health")
def health():
    return {"ok": True}
# 🔹 Ruta raíz (útil en navegador/Render)
@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is running 🚀"}
app.include_router(auth_router.router)

app.include_router(diagramas.router)
app.include_router(classes.router)
app.include_router(atributos.router)
app.include_router(metodo.router)
app.include_router(relacion.router)
app.include_router(export.router)
# Router WebSocket (colaboración en tiempo real)
app.include_router(realtime.router)
app.include_router(imagen_uml.router)
app.include_router(ia_edicion.router)