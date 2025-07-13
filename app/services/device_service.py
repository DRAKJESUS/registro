from typing import Union, Dict, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import make_transient
from sqlalchemy import select
import logging

from ..models.device_model import Device
from ..models.assignment_model import AssignmentHistory
from ..schemas.device_schema import DeviceCreate, DeviceUpdate
from .port_repository import PortRepository

logger = logging.getLogger(__name__)

class DeviceService:
    @staticmethod
    async def create_device(db: AsyncSession, device_data: DeviceCreate) -> Device:
        try:
            device = Device(
                ip=device_data.ip,
                status=device_data.status,
                description=device_data.description,
                protocol=device_data.protocol,
                location_id=device_data.location_id
            )
            db.add(device)
            await db.commit()
            await db.refresh(device)

            # Si hay puertos, crear y asociarlos
            if device_data.ports:
                await PortRepository.replace_ports(db, device.id, device_data.ports)

            return device
        except Exception as e:
            await db.rollback()
            logger.error(f"Error al crear dispositivo: {e}")
            raise

    @staticmethod
    async def get_all_devices(db: AsyncSession) -> List[Device]:
        try:
            result = await db.execute(select(Device))
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error al obtener dispositivos: {e}")
            raise

    @staticmethod
    async def get_device(db: AsyncSession, device_id: int) -> Union[Device, None]:
        try:
            device = await db.get(Device, device_id)
            if device:
                await db.refresh(device)
            return device
        except Exception as e:
            logger.error(f"Error al obtener dispositivo {device_id}: {e}")
            raise

    @staticmethod
    async def delete_device(db: AsyncSession, device_id: int):
        try:
            device = await db.get(Device, device_id)
            if not device:
                return {"error": "Dispositivo no encontrado"}
            await db.delete(device)
            await db.commit()
            return {"mensaje": "Dispositivo eliminado correctamente"}
        except Exception as e:
            await db.rollback()
            logger.error(f"Error al eliminar dispositivo {device_id}: {e}")
            raise

    @staticmethod
    async def update_device(db: AsyncSession, device_id: int, device_data: Union[DeviceUpdate, Dict[str, Any]]) -> Device:
        try:
            device = await db.get(Device, device_id)
            if not device:
                raise ValueError("Dispositivo no encontrado")

            data = device_data.dict(exclude_unset=True) if not isinstance(device_data, dict) else device_data

            old_status = device.status
            old_location = device.location_id

            for field in ["ip", "status", "description", "protocol", "location_id"]:
                if field in data:
                    setattr(device, field, data[field])

            if "ports" in data:
                await PortRepository.replace_ports(db, device.id, data["ports"])

            # Registrar historial si hubo cambio
            if ("status" in data and data["status"] != old_status) or \
               ("location_id" in data and data["location_id"] != old_location):
                history = AssignmentHistory(
                    device_id=device.id,
                    action="ACTUALIZACIÓN DE DISPOSITIVO",
                    old_status=old_status,
                    new_status=device.status,
                    old_location_id=old_location,
                    new_location_id=device.location_id
                )
                db.add(history)

            db.add(device)
            await db.commit()
            await db.refresh(device)
            return device

        except Exception as e:
            await db.rollback()
            logger.error(f"Error al actualizar dispositivo {device_id}: {e}")
            raise
