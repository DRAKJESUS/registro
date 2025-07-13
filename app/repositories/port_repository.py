from sqlalchemy import delete
from ..models.port_model import Port
from ..schemas.port_schema import PortCreate

class PortRepository:
    @staticmethod
    async def replace_ports(
        db: AsyncSession,
        device_id: int,
        new_ports: List[Union[PortCreate, Dict[str, Any]]]
    ) -> List[Port]:
        try:
            # 1. Eliminar directamente todos los puertos relacionados
            await db.execute(delete(Port).where(Port.device_id == device_id))
            await db.commit()

            # 2. Crear nuevos objetos desde cero
            ports_to_create = []
            for port_data in new_ports:
                if isinstance(port_data, dict):
                    port_data = PortCreate(**port_data)

                ports_to_create.append(Port(
                    device_id=device_id,
                    port_number=port_data.port_number,
                    description=port_data.description
                ))

            db.add_all(ports_to_create)
            await db.commit()

            logger.info(f"Reemplazados puertos del dispositivo {device_id}")
            return ports_to_create

        except Exception as e:
            await db.rollback()
            logger.error(f"Error al reemplazar puertos del dispositivo {device_id}: {e}")
            raise
