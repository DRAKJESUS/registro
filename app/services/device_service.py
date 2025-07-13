from typing import Union, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete
from sqlalchemy.orm import make_transient
import logging
from ..models.port_model import Port
from ..models.device_model import Device
from ..models.assignment_model import AssignmentHistory
from ..schemas.device_schema import DeviceUpdate, DeviceCreate
from ..schemas.port_schema import PortCreate

logger = logging.getLogger(__name__)

class PortRepository:
    @staticmethod
    async def get_by_device(db: AsyncSession, device_id: int) -> List[Port]:
        """Obtiene todos los puertos de un dispositivo"""
        try:
            result = await db.execute(select(Port).where(Port.device_id == device_id))
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error al obtener puertos: {str(e)}")
            raise

    @staticmethod
    async def replace_ports(db: AsyncSession, device_id: int, new_ports: List[Union[PortCreate, Dict[str, Any]]]) -> List[Port]:
        """
        Reemplaza todos los puertos de un dispositivo de manera segura
        
        Args:
            db: Sesión de base de datos
            device_id: ID del dispositivo
            new_ports: Lista de nuevos puertos (objetos PortCreate o diccionarios)
        """
        try:
            # 1. Obtener y eliminar puertos existentes
            existing_ports = await PortRepository.get_by_device(db, device_id)
            for port in existing_ports:
                await db.delete(port)
            await db.commit()

            # 2. Crear nuevos puertos
            created_ports = []
            for port_data in new_ports:
                # Convertir diccionario a objeto PortCreate si es necesario
                if isinstance(port_data, dict):
                    port_data = PortCreate(**port_data)
                
                new_port = Port(
                    device_id=device_id,
                    port_number=port_data.port_number,
                    description=port_data.description,
                    protocol=getattr(port_data, 'protocol', None)
                )
                db.add(new_port)
                created_ports.append(new_port)
            
            await db.commit()
            
            # 3. Refrescar y retornar los nuevos puertos
            for port in created_ports:
                await db.refresh(port)
            
            logger.info(f"Reemplazados {len(existing_ports)} puertos con {len(created_ports)} nuevos")
            return created_ports
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error al reemplazar puertos: {str(e)}")
            raise

class DeviceService:
    @staticmethod
    async def _handle_assignment_change(
        db: AsyncSession, 
        device: Device, 
        action: str,
        **kwargs
    ) -> None:
        """Registra cambios importantes en el historial"""
        try:
            history = AssignmentHistory(
                device_id=device.id,
                action=action,
                **kwargs
            )
            db.add(history)
            await db.commit()
        except Exception as e:
            await db.rollback()
            logger.error(f"Error al registrar en historial: {str(e)}")
            raise

    @staticmethod
    async def get_device(db: AsyncSession, device_id: int) -> Union[Device, None]:
        """Obtiene un dispositivo por su ID"""
        try:
            device = await db.get(Device, device_id)
            if device:
                await db.refresh(device)
            return device
        except Exception as e:
            logger.error(f"Error al obtener dispositivo: {str(e)}")
            raise

    @staticmethod
    async def create_device(db: AsyncSession, device_data: DeviceCreate) -> Device:
        """Crea un nuevo dispositivo"""
        try:
            device = Device(**device_data.dict())
            db.add(device)
            await db.commit()
            await db.refresh(device)
            logger.info(f"Dispositivo creado: ID {device.id}")
            return device
        except Exception as e:
            await db.rollback()
            logger.error(f"Error al crear dispositivo: {str(e)}")
            raise

    @staticmethod
    async def update_device(db: AsyncSession, device_id: int, device_data: Union[DeviceUpdate, Dict[str, Any]]) -> Device:
        """
        Actualiza un dispositivo existente
        
        Args:
            db: Sesión de base de datos
            device_id: ID del dispositivo a actualizar
            device_data: Datos de actualización (DeviceUpdate o dict)
            
        Returns:
            Device: Dispositivo actualizado
            
        Raises:
            ValueError: Si el dispositivo no existe o datos inválidos
            SQLAlchemyError: Para errores de base de datos
        """
        try:
            # 1. Verificar existencia del dispositivo
            device = await DeviceService.get_device(db, device_id)
            if not device:
                raise ValueError("Dispositivo no encontrado")

            # 2. Preparar datos de actualización
            if isinstance(device_data, dict):
                update_data = device_data
            else:
                update_data = device_data.dict(exclude_unset=True)

            # 3. Guardar valores antiguos para historial
            old_values = {
                'location_id': device.location_id,
                'status': device.status,
                'ip': device.ip,
                'description': device.description,
                'protocol': device.protocol
            }

            # 4. Actualizar campos del dispositivo
            for field in ['ip', 'status', 'description', 'protocol', 'location_id']:
                if field in update_data:
                    setattr(device, field, update_data[field])

            # 5. Manejar actualización de puertos si existe
            if 'ports' in update_data:
                ports_data = update_data['ports']
                if not isinstance(ports_data, list):
                    ports_data = [ports_data]
                await PortRepository.replace_ports(db, device.id, ports_data)

            # 6. Registrar en historial si hubo cambios importantes
            history_updates = {}
            if 'status' in update_data and update_data['status'] != old_values['status']:
                history_updates.update({
                    'old_status': old_values['status'],
                    'new_status': device.status
                })
                
            if 'location_id' in update_data and update_data['location_id'] != old_values['location_id']:
                history_updates.update({
                    'old_location_id': old_values['location_id'],
                    'new_location_id': device.location_id
                })

            if history_updates:
                await DeviceService._handle_assignment_change(
                    db, device,
                    "ACTUALIZACIÓN DE DISPOSITIVO",
                    **history_updates
                )

            # 7. Confirmar cambios
            await db.commit()
            await db.refresh(device)
            
            logger.info(f"Dispositivo {device_id} actualizado exitosamente")
            return device
            
        except ValueError as ve:
            await db.rollback()
            logger.error(f"Error de validación: {str(ve)}")
            raise
        except SQLAlchemyError as sae:
            await db.rollback()
            logger.error(f"Error de base de datos: {str(sae)}")
            raise
        except Exception as e:
            await db.rollback()
            logger.error(f"Error inesperado: {str(e)}")
            raise

    @staticmethod
    async def delete_device(db: AsyncSession, device_id: int) -> Dict[str, str]:
        """Elimina un dispositivo"""
        try:
            device = await DeviceService.get_device(db, device_id)
            if not device:
                raise ValueError("Dispositivo no encontrado")
                
            make_transient(device)  # Prevenir problemas con la sesión
            await db.delete(device)
            await db.commit()
            
            logger.info(f"Dispositivo {device_id} eliminado")
            return {"message": "Dispositivo eliminado correctamente"}
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error al eliminar dispositivo: {str(e)}")
            raise

    @staticmethod
    async def get_all_devices(db: AsyncSession) -> List[Device]:
        """Obtiene todos los dispositivos"""
        try:
            result = await db.execute(select(Device))
            devices = result.scalars().all()
            
            # Refrescar cada dispositivo para asegurar consistencia
            for device in devices:
                await db.refresh(device)
                
            return devices
        except Exception as e:
            logger.error(f"Error al obtener dispositivos: {str(e)}")
            raise