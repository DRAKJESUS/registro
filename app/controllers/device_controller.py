from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..schemas.device_schema import DeviceCreate, DeviceOut
from ..services.device_service import DeviceService
from ..database import get_session

router = APIRouter(prefix="/devices", tags=["Dispositivos"])

@router.post("/", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
async def create_device(device: DeviceCreate, db: AsyncSession = Depends(get_session)):
    """
    Crea un nuevo dispositivo con IP, tipo, descripción, protocolo, puertos y localización (opcional).
    """
    return await DeviceService.create_device(db, device)

@router.get("/", response_model=List[DeviceOut])
async def list_devices(db: AsyncSession = Depends(get_session)):
    """
    Lista todos los dispositivos registrados con sus puertos y localización.
    """
    return await DeviceService.get_devices(db)

@router.delete("/{device_id}")
async def delete_device(device_id: int, db: AsyncSession = Depends(get_session)):
    """
    Elimina un dispositivo por su ID.
    """
    return await DeviceService.delete(db, device_id)

@router.post("/{device_id}/assign/{location_id}")
async def assign_device(device_id: int, location_id: int, db: AsyncSession = Depends(get_session)):
    """
    Asigna un dispositivo a una localización.
    """
    return await DeviceService.assign_location(db, device_id, location_id)

@router.post("/{device_id}/change/{location_id}")
async def change_device_location(device_id: int, location_id: int, db: AsyncSession = Depends(get_session)):
    """
    Cambia la localización de un dispositivo.
    """
    return await DeviceService.change_location(db, device_id, location_id)

@router.put("/{device_id}/status")
async def update_device_status(device_id: int, status: str, db: AsyncSession = Depends(get_session)):
    """
    Cambia el status del dispositivo y guarda el cambio en historial.
    """
    return await DeviceService.update_status(db, device_id, status)
