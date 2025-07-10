from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..schemas.location_schema import LocationCreate, LocationOut
from ..services.location_service import LocationService
from ..database import get_session

router = APIRouter(prefix="/locations", tags=["Localizaciones"])

@router.post("/", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
async def create_location(location: LocationCreate, db: AsyncSession = Depends(get_session)):
    return await LocationService.create(db, location)

@router.get("/", response_model=List[LocationOut])
async def list_locations(db: AsyncSession = Depends(get_session)):
    return await LocationService.get_all(db)
