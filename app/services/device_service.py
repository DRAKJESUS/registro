from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.device_schema import DeviceCreate, DeviceUpdate
from ..repositories.device_repository import DeviceRepository
from ..repositories.port_repository import PortRepository
from ..models.assignment_model import AssignmentHistory
from ..models.device_model import Device

class DeviceService:
    @staticmethod
    async def create_device(db: AsyncSession, device: DeviceCreate):
        return await DeviceRepository.create(db, device)

    @staticmethod
    async def get_devices(db: AsyncSession):
        return await DeviceRepository.get_all(db)

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
        old = device.location_id
        device.location_id = location_id

        history = AssignmentHistory(
            device_id=device.id,
            action="ASIGNACIÓN",
            old_location_id=old,
            new_location_id=location_id
        )
        db.add(history)
        db.add(device)
        await db.commit()
        return {"mensaje": "Dispositivo asignado a localización"}

    @staticmethod
    async def change_location(db: AsyncSession, device_id: int, location_id: int):
        device = await db.get(Device, device_id)
        if not device:
            return {"error": "Dispositivo no encontrado"}
        old = device.location_id
        device.location_id = location_id

        history = AssignmentHistory(
            device_id=device.id,
            action="CAMBIO DE LOCALIZACIÓN",
            old_location_id=old,
            new_location_id=location_id
        )
        db.add(history)
        db.add(device)
        await db.commit()
        return {"mensaje": "Localización cambiada"}

    @staticmethod
    async def change_status(db: AsyncSession, device_id: int, status: str):
        device = await db.get(Device, device_id)
        if not device:
            return {"error": "Dispositivo no encontrado"}
        old = device.status
        device.status = status

        history = AssignmentHistory(
            device_id=device.id,
            action="CAMBIO DE ESTATUS",
            old_status=old,
            new_status=status
        )
        db.add(history)
        db.add(device)
        await db.commit()
        return {"mensaje": f"Estatus actualizado a {status}"}

    @staticmethod
    async def update_device(db: AsyncSession, device_id: int, device_data: DeviceUpdate):
        device = await db.get(Device, device_id)
        if not device:
            return {"error": "Dispositivo no encontrado"}

        old_location = device.location_id
        old_status = device.status

        # Actualización de campos si vienen en la petición
        if device_data.ip is not None:
            device.ip = device_data.ip
        if device_data.status is not None:
            device.status = device_data.status
        if device_data.description is not None:
            device.description = device_data.description
        if device_data.protocol is not None:
            device.protocol = device_data.protocol
        if device_data.location_id is not None:
            device.location_id = device_data.location_id

        # 🚨 IMPORTANTE: reemplazar puertos SOLO después del commit del delete
        if device_data.ports is not None:
            await PortRepository.replace_ports(db, device.id, device_data.ports)

        # Si cambió status o localización, registrar historial
        if (device_data.status and device_data.status != old_status) or \
           (device_data.location_id and device_data.location_id != old_location):
            history = AssignmentHistory(
                device_id=device.id,
                action="ACTUALIZACIÓN DE DISPOSITIVO",
                old_location_id=old_location,
                new_location_id=device.location_id,
                old_status=old_status,
                new_status=device.status
            )
            db.add(history)

        db.add(device)
        await db.commit()
        await db.refresh(device)
        return device
