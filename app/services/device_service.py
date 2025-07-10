from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from ..schemas.device_schema import DeviceCreate
from ..repositories.device_repository import DeviceRepository
from ..models.assignment_model import AssignmentHistory
from ..models.device_model import Device
from ..models.location_model import Location


class DeviceService:
    @staticmethod
    async def create_device(db: AsyncSession, device: DeviceCreate):
        return await DeviceRepository.create(db, device)

    @staticmethod
    async def get_devices(db: AsyncSession):
        result = await db.execute(
            select(Device)
            .options(selectinload(Device.ports), selectinload(Device.location))
        )
        return result.scalars().all()

    @staticmethod
    async def delete(db: AsyncSession, device_id: int):
        device = await db.get(Device, device_id)
        if not device:
            return {"error": "Dispositivo no encontrado"}
        await db.delete(device)
        await db.commit()
        return {"mensaje": "Dispositivo eliminado"}

    @staticmethod
    async def assign_location(db: AsyncSession, device_id: int, location_id: int):
        device = await db.get(Device, device_id)
        if not device:
            return {"error": "Dispositivo no encontrado"}
        device.location_id = location_id
        db.add(AssignmentHistory(device_id=device_id, new_location_id=location_id, action="ASIGNADO"))
        await db.commit()
        return {"mensaje": "Dispositivo asignado a localización"}

    @staticmethod
    async def change_location(db: AsyncSession, device_id: int, location_id: int):
        device = await db.get(Device, device_id)
        if not device:
            return {"error": "Dispositivo no encontrado"}
        old = getattr(device, 'location_id', None)
        device.location_id = location_id
        db.add(AssignmentHistory(device_id=device_id, old_location_id=old, new_location_id=location_id, action="CAMBIO"))
        await db.commit()
        return {"mensaje": "Localización cambiada"}
