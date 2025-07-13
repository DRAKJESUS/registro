from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Importaciones de routers
from app.controllers import (
    device_controller,
    location_controller,
    assignment_controller,
    history_controller,
)

# Base de datos y modelos
from app.database import engine, Base

# Manejadores de excepciones
from app.exceptions import (
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

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto si vas a producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas al iniciar
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Incluir rutas
app.include_router(device_controller.router)
app.include_router(location_controller.router)
app.include_router(assignment_controller.router)
app.include_router(history_controller.router)

# Manejo de errores
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(IntegrityError, integrity_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Para ejecución local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000, reload=True)
