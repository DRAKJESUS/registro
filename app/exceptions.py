from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"error": "Error de validación", "detalles": exc.errors()}
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Error en la base de datos", "detalles": str(exc)}
    )


async def integrity_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"error": "Violación de integridad", "detalles": str(exc.orig)}
    )


async def not_found_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=HTTP_404_NOT_FOUND,
        content={"error": "Recurso no encontrado"}
    )