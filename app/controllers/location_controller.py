from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.location_schema import LocationCreate, LocationOut
from ..services.location_service import LocationService
from ..database import SessionLocal

router = APIRouter(prefix="/locations", tags=["Localizaciones"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", response_model=LocationOut, summary="Crear localización", description="Crea una nueva localización o grupo.")
async def create_location(loc: LocationCreate, db: AsyncSession = Depends(get_db)):
    return await LocationService.create(db, loc)

@router.get("/", response_model=list[LocationOut], summary="Listar localizaciones", description="Obtiene una lista de todas las localizaciones registradas.")
async def list_locations(db: AsyncSession = Depends(get_db)):
    return await LocationService.get_all(db)