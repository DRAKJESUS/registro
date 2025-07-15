from typing import Union, Dict, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import logging

from ..models.device_model import Device
from ..models.assignment_model import AssignmentHistory
from ..schemas.device_schema import DeviceCreate, DeviceUpdate
from ..repositories.port_repository import PortRepository

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
            await db.flush()
            await db.refresh(device)

            if device_data.ports:
                await PortRepository.replace_ports(db, device.id, device_data.ports)

            await db.commit()

            # Recargar relaciones (puertos y localización)
            result = await db.execute(
                select(Device).where(Device.id == device.id).options(
                    selectinload(Device.ports),
                    selectinload(Device.location)
                )
            )
            device = result.scalar_one()

            logger.info(f"Dispositivo creado: {device.id}")
            return device
        except Exception as e:
            await db.rollback()
            logger.error(f"Error al crear dispositivo: {e}")
            raise

    @staticmethod
    async def get_all_devices(db: AsyncSession) -> List[Device]:
        try:
            result = await db.execute(
                select(Device).options(
                    selectinload(Device.ports),
                    selectinload(Device.location)
                )
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error al obtener dispositivos: {e}")
            raise

    @staticmethod
    async def get_device(db: AsyncSession, device_id: int) -> Union[Device, None]:
        try:
            result = await db.execute(
                select(Device).where(Device.id == device_id).options(
                    selectinload(Device.ports),
                    selectinload(Device.location)
                )
            )
            return result.scalar_one_or_none()
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
            logger.info(f"Dispositivo eliminado: {device_id}")
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

            db.add(device)
            await db.flush()

            if "ports" in data:
                await PortRepository.replace_ports(db, device.id, data["ports"])

            history_fields = {}
            if "status" in data and data["status"] != old_status:
                history_fields["old_status"] = old_status
                history_fields["new_status"] = device.status
            if "location_id" in data and data["location_id"] != old_location:
                history_fields["old_location_id"] = old_location
                history_fields["new_location_id"] = device.location_id

            if history_fields:
                history = AssignmentHistory(
                    device_id=device.id,
                    action="ACTUALIZACIÓN DE DISPOSITIVO",
                    **history_fields
                )
                db.add(history)

            await db.commit()
            await db.refresh(device)

            result = await db.execute(
                select(Device).where(Device.id == device.id).options(
                    selectinload(Device.ports),
                    selectinload(Device.location)
                )
            )
            device = result.scalar_one()

            logger.info(f"Dispositivo actualizado: {device_id}")
            return device

        except ValueError as ve:
            await db.rollback()
            logger.warning(f"Validación fallida: {ve}")
            raise
        except SQLAlchemyError as sae:
            await db.rollback()
            logger.error(f"Error en base de datos al actualizar dispositivo: {sae}")
            raise
        except Exception as e:
            await db.rollback()
            logger.error(f"Error inesperado al actualizar dispositivo {device_id}: {e}")
            raise

    @staticmethod
    async def change_status(db: AsyncSession, device_id: int, new_status: str):
        try:
            device = await db.get(Device, device_id)
            if not device:
                raise ValueError("Dispositivo no encontrado")

            old_status = device.status
            if old_status == new_status:
                return {"mensaje": f"El dispositivo ya tiene el estado '{new_status}'"}

            device.status = new_status

            history = AssignmentHistory(
                device_id=device.id,
                action="CAMBIO DE STATUS",
                old_status=old_status,
                new_status=new_status,
                old_location_id=device.location_id,
                new_location_id=device.location_id
            )
            db.add(history)
            await db.commit()
            await db.refresh(device)
            return device

        except Exception as e:
            await db.rollback()
            logger.error(f"Error al cambiar status del dispositivo {device_id}: {e}")
            raise

    @staticmethod
    async def assign_location(db: AsyncSession, device_id: int, location_id: int):
        try:
            device = await db.get(Device, device_id)
            if not device:
                raise ValueError("Dispositivo no encontrado")

            if device.location_id == location_id:
                return {"mensaje": f"El dispositivo ya está en la localización {location_id}"}

            history = AssignmentHistory(
                device_id=device.id,
                action="ASIGNACIÓN DE LOCALIZACIÓN",
                old_location_id=device.location_id,
                new_location_id=location_id,
                old_status=device.status,
                new_status=device.status
            )

            device.location_id = location_id
            db.add(device)
            db.add(history)
            await db.commit()
            await db.refresh(device)
            return device

        except Exception as e:
            await db.rollback()
            logger.error(f"Error al asignar localización al dispositivo {device_id}: {e}")
            raise

    @staticmethod
    async def change_location(db: AsyncSession, device_id: int, location_id: int):
        try:
            device = await db.get(Device, device_id)
            if not device:
                raise ValueError("Dispositivo no encontrado")

            if device.location_id == location_id:
                return {"mensaje": f"El dispositivo ya está en la localización {location_id}"}

            history = AssignmentHistory(
                device_id=device.id,
                action="CAMBIO DE LOCALIZACIÓN",
                old_location_id=device.location_id,
                new_location_id=location_id,
                old_status=device.status,
                new_status=device.status
            )

            device.location_id = location_id
            db.add(device)
            db.add(history)
            await db.commit()
            await db.refresh(device)
            return device

        except Exception as e:
            await db.rollback()
            logger.error(f"Error al cambiar localización del dispositivo {device_id}: {e}")
            raise

    @staticmethod
    async def get(db: AsyncSession, device_id: int) -> Device:
        try:
            result = await db.execute(
                select(Device).where(Device.id == device_id).options(
                    selectinload(Device.ports),
                    selectinload(Device.location)
                )
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error al obtener dispositivo {device_id}: {e}")
            raise
