from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import SessionLocal
from ..services.assignment_service import AssignmentService
from ..schemas.assignment_schema import AssignmentOut

router = APIRouter(prefix="/history", tags=["Historial de asignaciones"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[AssignmentOut], summary="Consultar historial", description="Obtiene el historial de asignaciones y cambios de localización.")
async def get_history(db: AsyncSession = Depends(get_db)):
    return await AssignmentService.get_all(db)

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..schemas.assignment_schema import AssignmentOut
from ..services.assignment_service import AssignmentService
from ..database import get_session

router = APIRouter(prefix="/history", tags=["Historial"])

@router.get("/", response_model=List[AssignmentOut])
async def get_history(db: AsyncSession = Depends(get_session)):
    """
    Devuelve el historial completo de asignaciones y cambios de status de todos los dispositivos.
    """
    return await AssignmentService.get_all_history(db)
