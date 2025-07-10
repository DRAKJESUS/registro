from fastapi import FastAPI, Request
from .controllers import device_controller, location_controller, assignment_controller
from .database import engine, Base
from .exceptions import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    integrity_exception_handler
)
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi.exceptions import RequestValidationError

app = FastAPI(
    title="API de Inventario de Dispositivos",
    description="""
Sistema para gestionar dispositivos de red, asignarlos a localizaciones (grupos),
y llevar un historial completo de cambios y asignaciones.
""",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(device_controller.router)
app.include_router(location_controller.router)
app.include_router(assignment_controller.router)

# Registrar manejadores de errores
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(IntegrityError, integrity_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
