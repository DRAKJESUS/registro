from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from typing import List
from ..models.port_model import Port
from ..schemas.port_schema import PortCreate

class PortRepository:
    @staticmethod
    async def replace_ports(db: AsyncSession, device_id: int, new_ports: List[PortCreate]):
        # Borra todos los puertos del dispositivo
        await db.execute(delete(Port).where(Port.device_id == device_id))
        await db.flush()  # 🔧 Esto es lo que evita el error del objeto eliminado

        # Inserta nuevos puertos
        for port_data in new_ports:
            port = Port(
                device_id=device_id,
                port_number=port_data.port_number,
                description=port_data.description
            )
            db.add(port)
