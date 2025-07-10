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