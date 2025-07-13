from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Union
import logging
from ..models.port_model import Port
from ..schemas.port_schema import PortCreate, PortSchema

logger = logging.getLogger(__name__)

class PortRepository:
    @staticmethod
    async def replace_ports(db: AsyncSession, device_id: int, new_ports: List[Union[PortCreate, dict]]):
        """
        Reemplaza todos los puertos de un dispositivo de manera segura
        Acepta tanto objetos PortCreate como diccionarios
        """
        try:
            # 1. Obtener puertos existentes
            result = await db.execute(select(Port).where(Port.device_id == device_id))
            existing_ports = result.scalars().all()
            
            logger.debug(f"Puertos existentes a reemplazar: {len(existing_ports)}")
            
            # 2. Eliminar puertos existentes
            for port in existing_ports:
                await db.delete(port)
            
            await db.commit()
            
            # 3. Crear nuevos puertos
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
            
            # Refrescar los objetos para asegurar consistencia
            for port in created_ports:
                await db.refresh(port)
            
            logger.debug(f"Puertos creados exitosamente: {len(created_ports)}")
            return created_ports
            
        except Exception as e:
            logger.error(f"Error al reemplazar puertos: {str(e)}")
            await db.rollback()
            raise