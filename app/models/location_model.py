from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.location_schema import LocationCreate, LocationOut
from ..services.location_service import LocationService
from ..database import get_session

router = APIRouter(prefix="/locations", tags=["Localizaciones"])


@router.post("/", response_model=LocationOut)
async def create_location(location: LocationCreate, db: AsyncSession = Depends(get_session)):
    return await LocationService.create(db, location)


@router.get("/", response_model=list[LocationOut])
async def get_locations(db: AsyncSession = Depends(get_session)):
    return await LocationService.get_all(db)

@router.put("/{location_id}", response_model=LocationOut)
async def update_location(location_id: int, location: LocationCreate, db: AsyncSession = Depends(get_session)):
    updated = await LocationService.update(db, location_id, location)
    if not updated:
        raise HTTPException(status_code=404, detail="Localización no encontrada")
    return updated


@router.delete("/{location_id}")
async def delete_location(location_id: int, db: AsyncSession = Depends(get_session)):
    result = await LocationService.delete(db, location_id)
    if not result:
        raise HTTPException(status_code=404, detail="Localización no encontrada")
    return {"mensaje": "Localización eliminada correctamente"}
