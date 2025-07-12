from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.location_schema import LocationCreate, LocationOut
from ..services.location_service import LocationService
from ..database import get_session

router = APIRouter(prefix="/locations", tags=["Localizaciones"])

@router.post("/", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
async def create_location(location: LocationCreate, db: AsyncSession = Depends(get_session)):
    """
    Crea una nueva localización.

    - **name**: nombre único de la ubicación (ej. "Oficina principal")
    - **description**: descripción opcional de la ubicación
    """
    return await LocationService.create(db, location)

@router.get("/", response_model=list[LocationOut])
async def get_locations(db: AsyncSession = Depends(get_session)):
    """
    Retorna todas las localizaciones existentes.
    """
    return await LocationService.get_all(db)

@router.put("/{location_id}", response_model=LocationOut)
async def update_location(location_id: int, location: LocationCreate, db: AsyncSession = Depends(get_session)):
    """
    Edita una localización por ID.

    - **location_id**: ID numérico de la localización a actualizar
    - **name**: nuevo nombre
    - **description**: nueva descripción
    """
    updated = await LocationService.update(db, location_id, location)
    if not updated:
        raise HTTPException(status_code=404, detail="Localización no encontrada")
    return updated

@router.delete("/{location_id}")
async def delete_location(location_id: int, db: AsyncSession = Depends(get_session)):
    """
    Elimina una localización por su ID.

    ⚠️ Nota: También se eliminarán los dispositivos vinculados a esta ubicación si existen.
    """
    result = await LocationService.delete(db, location_id)
    if not result:
        raise HTTPException(status_code=404, detail="Localización no encontrada")
    return {"mensaje": "Localización eliminada correctamente"}
