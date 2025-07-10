from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.device_schema import DeviceCreate, DeviceOut
from ..services.device_service import DeviceService
from ..database import SessionLocal

router = APIRouter(prefix="/devices", tags=["Dispositivos"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", response_model=DeviceOut, summary="Registrar dispositivo", description="Crea un nuevo dispositivo con sus puertos asociados.")
async def create_device(device: DeviceCreate, db: AsyncSession = Depends(get_db)):
    return await DeviceService.create_device(db, device)

@router.get("/", response_model=list[DeviceOut], summary="Listar dispositivos", description="Obtiene una lista de todos los dispositivos registrados.")
async def get_devices(db: AsyncSession = Depends(get_db)):
    return await DeviceService.get_devices(db)

@router.delete("/{device_id}", summary="Eliminar dispositivo", description="Elimina un dispositivo por su ID.")
async def delete_device(device_id: int, db: AsyncSession = Depends(get_db)):
    return await DeviceService.delete(db, device_id)

@router.put("/{device_id}/assign/{location_id}", summary="Asignar dispositivo", description="Asigna un dispositivo a una localización específica.")
async def assign_device(device_id: int, location_id: int, db: AsyncSession = Depends(get_db)):
    return await DeviceService.assign_location(db, device_id, location_id)

@router.put("/{device_id}/change-location/{location_id}", summary="Cambiar localización", description="Cambia la localización asignada a un dispositivo.")
async def change_device_location(device_id: int, location_id: int, db: AsyncSession = Depends(get_db)):
    return await DeviceService.change_location(db, device_id, location_id)