from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import make_transient
import logging
from ..schemas.device_schema import DeviceCreate, DeviceUpdate
from ..repositories.device_repository import DeviceRepository
from ..repositories.port_repository import PortRepository
from ..models.assignment_model import AssignmentHistory
from ..models.device_model import Device

logger = logging.getLogger(__name__)

class DeviceService:
    @staticmethod
    async def create_device(db: AsyncSession, device: DeviceCreate):
        try:
            new_device = await DeviceRepository.create(db, device)
            await db.commit()
            await db.refresh(new_device)
            return new_device
        except Exception as e:
            await db.rollback()
            logger.error(f"Error al crear dispositivo: {str(e)}")
            raise

    @staticmethod
    async def get_devices(db: AsyncSession):
        try:
            devices = await DeviceRepository.get_all(db)
            return devices
        except Exception as e:
            logger.error(f"Error al obtener dispositivos: {str(e)}")
            raise

    @staticmethod
    async def delete(db: AsyncSession, device_id: int):
        try:
            device = await db.get(Device, device_id)
            if not device:
                logger.warning(f"Dispositivo no encontrado: ID {device_id}")
                return {"error": "Dispositivo no encontrado"}
            
            # Hacer transient para evitar problemas con la sesión
            make_transient(device)
            
            await db.delete(device)
            await db.commit()
            return {"mensaje": "Dispositivo eliminado"}
        except Exception as e:
            await db.rollback()
            logger.error(f"Error al eliminar dispositivo: {str(e)}")
            raise

    @staticmethod
    async def _handle_assignment_change(db: AsyncSession, device: Device, action: str, 
                                      old_location_id: int = None, new_location_id: int = None,
                                      old_status: str = None, new_status: str = None):
        """Método helper para manejar cambios de asignación"""
        history = AssignmentHistory(
            device_id=device.id,
            action=action,
            old_location_id=old_location_id,
            new_location_id=new_location_id,
            old_status=old_status,
            new_status=new_status
        )
        db.add(history)
        db.add(device)
        await db.commit()
        await db.refresh(device)

    @staticmethod
    async def assign_location(db: AsyncSession, device_id: int, location_id: int):
        try:
            device = await db.get(Device, device_id)
            if not device:
                logger.warning(f"Dispositivo no encontrado para asignación: ID {device_id}")
                return {"error": "Dispositivo no encontrado"}
            
            old_location = device.location_id
            device.location_id = location_id
            
            await DeviceService._handle_assignment_change(
                db, device, "ASIGNACIÓN",
                old_location_id=old_location,
                new_location_id=location_id
            )
            
            return {"mensaje": "Dispositivo asignado a localización"}
        except Exception as e:
            await db.rollback()
            logger.error(f"Error al asignar localización: {str(e)}")
            raise

    @staticmethod
    async def change_location(db: AsyncSession, device_id: int, location_id: int):
        try:
            device = await db.get(Device, device_id)
            if not device:
                logger.warning(f"Dispositivo no encontrado para cambio: ID {device_id}")
                return {"error": "Dispositivo no encontrado"}
            
            old_location = device.location_id
            device.location_id = location_id
            
            await DeviceService._handle_assignment_change(
                db, device, "CAMBIO DE LOCALIZACIÓN",
                old_location_id=old_location,
                new_location_id=location_id
            )
            
            return {"mensaje": "Localización cambiada"}
        except Exception as e:
            await db.rollback()
            logger.error(f"Error al cambiar localización: {str(e)}")
            raise

    @staticmethod
    async def change_status(db: AsyncSession, device_id: int, status: str):
        try:
            device = await db.get(Device, device_id)
            if not device:
                logger.warning(f"Dispositivo no encontrado para cambio de estado: ID {device_id}")
                return {"error": "Dispositivo no encontrado"}
            
            old_status = device.status
            device.status = status
            
            await DeviceService._handle_assignment_change(
                db, device, "CAMBIO DE ESTATUS",
                old_status=old_status,
                new_status=status
            )
            
            return {"mensaje": f"Estatus actualizado a {status}"}
        except Exception as e:
            await db.rollback()
            logger.error(f"Error al cambiar estado: {str(e)}")
            raise

    @staticmethod
    async def update_device(db: AsyncSession, device_id: int, device_data: DeviceUpdate):
        try:
            device = await db.get(Device, device_id)
            if not device:
                logger.warning(f"Dispositivo no encontrado para actualización: ID {device_id}")
                return {"error": "Dispositivo no encontrado"}

            # Guardar valores antiguos
            old_values = {
                "location_id": device.location_id,
                "status": device.status,
                "ip": device.ip,
                "description": device.description,
                "protocol": device.protocol
            }

            # Actualizar campos modificados
            update_fields = device_data.dict(exclude_unset=True)
            for field, value in update_fields.items():
                if field != "ports":  # Los puertos se manejan aparte
                    setattr(device, field, value)

            # Manejo de puertos en transacción separada
            if "ports" in update_fields:
                await PortRepository.replace_ports(db, device.id, update_fields["ports"])

            # Registrar historial si hay cambios relevantes
            if (update_fields.get("status") and update_fields["status"] != old_values["status"]) or \
               (update_fields.get("location_id") and update_fields["location_id"] != old_values["location_id"]):
                
                await DeviceService._handle_assignment_change(
                    db, device, "ACTUALIZACIÓN DE DISPOSITIVO",
                    old_location_id=old_values["location_id"],
                    new_location_id=device.location_id,
                    old_status=old_values["status"],
                    new_status=device.status
                )

            await db.commit()
            await db.refresh(device)
            return device
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error al actualizar dispositivo: {str(e)}")
            raise