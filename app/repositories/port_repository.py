from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Union, Dict, Any
import logging

from ..models.port_model import Port
from ..schemas.port_schema import PortCreate

logger = logging.getLogger(__name__)

class PortRepository:
    @staticmethod
    async def replace_ports(
        db: AsyncSession,
        device_id: int,
        new_ports: List[Union[PortCreate, Dict[str, Any]]]
    ) -> List[Port]:
        try:
            # Leer puertos actuales
            result = await db.execute(
                select(Port).where(Port.device_id == device_id)
            )
            existing_ports = result.scalars().all()

            # Eliminar puertos existentes
            for port in existing_ports:
                await db.delete(port)

            await db.flush()  # Se asegura de que no haya conflictos antes del commit

            # Crear nuevos puertos
            created_ports = []
            for port_data in new_ports:
                if isinstance(port_data, dict):
                    port_data = PortCreate(**port_data)

                new_port = Port(
                    device_id=device_id,
                    port_number=port_data.port_number,
                    description=port_data.description
                )
                db.add(new_port)
                created_ports.append(new_port)

            await db.flush()
            for port in created_ports:
                await db.refresh(port)

            logger.info(f"Reemplazados puertos del dispositivo {device_id}")
            return created_ports

        except Exception as e:
            await db.rollback()
            logger.error(f"Error al reemplazar puertos del dispositivo {device_id}: {e}")
            raise
