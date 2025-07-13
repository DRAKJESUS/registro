from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..schemas.device_schema import DeviceCreate, DeviceOut, DeviceUpdate
from ..services.device_service import DeviceService
from ..database import get_session

router = APIRouter(prefix="/devices", tags=["Dispositivos"])

@router.post("/", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
async def create_device(device: DeviceCreate, db: AsyncSession = Depends(get_session)):
    try:
        return await DeviceService.create_device(db, device)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[DeviceOut])
async def list_devices(db: AsyncSession = Depends(get_session)):
    try:
        return await DeviceService.get_all_devices(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{device_id}")
async def delete_device(device_id: int, db: AsyncSession = Depends(get_session)):
    try:
        return await DeviceService.delete_device(db, device_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{device_id}/assign/{location_id}")
async def assign_device(device_id: int, location_id: int, db: AsyncSession = Depends(get_session)):
    try:
        return await DeviceService.assign_location(db, device_id, location_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{device_id}/change/{location_id}")
async def change_device_location(device_id: int, location_id: int, db: AsyncSession = Depends(get_session)):
    try:
        return await DeviceService.change_location(db, device_id, location_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{device_id}/status", response_model=DeviceOut)
async def update_device_status(device_id: int, status: str, db: AsyncSession = Depends(get_session)):
    try:
        return await DeviceService.change_status(db, device_id, status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{device_id}", response_model=DeviceOut)
async def update_device(device_id: int, device: DeviceUpdate, db: AsyncSession = Depends(get_session)):
    try:
        return await DeviceService.update_device(db, device_id, device)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
