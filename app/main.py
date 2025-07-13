from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from .controllers import (
    device_controller,
    location_controller,
    assignment_controller,
    history_controller,
)
from .database import engine, Base
from .exceptions import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    integrity_exception_handler,
)

app = FastAPI(
    title="API de Inventario de Dispositivos",
    description="""
Sistema para gestionar dispositivos de red, asignarlos a localizaciones (grupos),
y llevar un historial completo de cambios y asignaciones.
""",
    version="1.0.0",
)

# CORS Middleware (ajustado para producción si lo deseas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes especificar dominios en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos: creación de tablas (auto-inicialización en startup)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        # Puedes descomentar el drop_all si necesitas reiniciar la DB en desarrollo
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# Rutas (controladores)
app.include_router(device_controller.router)
app.include_router(location_controller.router)
app.include_router(assignment_controller.router)
app.include_router(history_controller.router)

# Manejadores de errores personalizados
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(IntegrityError, integrity_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Solo útil si ejecutas local directamente con `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000, reload=True)
