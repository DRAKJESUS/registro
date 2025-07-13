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
        """
        Reemplaza todos los puertos de un dispositivo.
        Elimina los actuales y crea nuevos desde cero.

        Args:
            db (AsyncSession): Sesión de la base de datos.
            device_id (int): ID del dispositivo.
            new_ports (List[Union[PortCreate, Dict[str, Any]]]): Lista de nuevos puertos.

        Returns:
            List[Port]: Lista de objetos Port recién creados.
        """
        try:
            # 1. Obtener puertos actuales
            result = await db.execute(
                select(Port).where(Port.device_id == device_id)
            )
            existing_ports = result.scalars().all()

            # 2. Eliminar puertos existentes
            for port in existing_ports:
                await db.delete(port)

            await db.commit()  # commit tras el delete

            # 3. Crear nuevos puertos
            created_ports = []
            for port_data in new_ports:
                if isinstance(port_data, dict):
                    port_data = PortCreate(**port_data)

                new_port = Port(
                    device_id=device_id,
                    port_number=port_data.port_number,
                    description=port_data.description,
                    protocol=getattr(port_data, "protocol", None)
                )
                db.add(new_port)
                created_ports.append(new_port)

            await db.commit()

            # 4. Refrescar solo los nuevos puertos
            for port in created_ports:
                await db.refresh(port)

            logger.info(f"Reemplazados puertos del dispositivo {device_id}")
            return created_ports

        except Exception as e:
            await db.rollback()
            logger.error(f"Error al reemplazar puertos del dispositivo {device_id}: {e}")
            raise
