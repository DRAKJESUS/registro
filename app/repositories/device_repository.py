from sqlalchemy.ext.asyncio import AsyncSession
from ..models.device_model import Device
from ..models.port_model import Port
from ..schemas.device_schema import DeviceCreate
from sqlalchemy.future import select

class DeviceRepository:
    @staticmethod
    async def create(db: AsyncSession, device_data: DeviceCreate):
        device = Device(
            ip=device_data.ip,
            type=device_data.type,
            description=device_data.description,
            protocol=device_data.protocol,
            location_id=device_data.location_id
        )
        db.add(device)
        await db.flush()  # obtiene el ID del dispositivo

        for port in device_data.ports:
            new_port = Port(
                port_number=port.port_number,
                description=port.description,
                device_id=device.id
            )
            db.add(new_port)

        await db.commit()
        await db.refresh(device)
        return device

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Device))
        return result.scalars().all()
