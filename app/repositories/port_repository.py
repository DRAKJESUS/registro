from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from typing import List
from ..models.port_model import Port
from ..schemas.port_schema import PortCreate

class PortRepository:
    @staticmethod
    async def replace_ports(db: AsyncSession, device_id: int, new_ports: List[PortCreate]):
        # Elimina todos los puertos existentes para el dispositivo
        await db.execute(delete(Port).where(Port.device_id == device_id))
        await db.flush()  # 👈 Esto es crucial para evitar el error 500

        # Inserta los nuevos puertos
        for port_data in new_ports:
            port = Port(
                device_id=device_id,
                port_number=port_data.port_number,
                description=port_data.description
            )
            db.add(port)

        # No commit aquí, lo hace DeviceService
