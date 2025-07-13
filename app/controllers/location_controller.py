from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..schemas.location_schema import LocationCreate, LocationOut
from ..services.location_service import LocationService
from ..database import get_session

router = APIRouter(prefix="/locations", tags=["Localizaciones"])

@router.post("/", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
async def create_location(location: LocationCreate, db: AsyncSession = Depends(get_session)):
    """
    Crea una nueva localización si no existe una con el mismo nombre.
    """
    existing = await LocationService.get_by_name(db, location.name)
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe una localización con ese nombre")
    
    return await LocationService.create(db, location)

@router.get("/", response_model=List[LocationOut])
async def list_locations(db: AsyncSession = Depends(get_session)):
    """
    Lista todas las localizaciones disponibles.
    """
    return await LocationService.get_all(db)

@router.get("/{location_id}", response_model=LocationOut)
async def get_location(location_id: int, db: AsyncSession = Depends(get_session)):
    """
    Obtiene una localización por ID.
    """
    location = await LocationService.get(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Localización no encontrada")
    return location
