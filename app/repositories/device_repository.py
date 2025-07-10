from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.device_model import Device, Port
from ..schemas.device_schema import DeviceCreate


class DeviceRepository:
    @staticmethod
    async def create(db: AsyncSession, device_data: DeviceCreate):
        device = Device(
            ip=device_data.ip,
            type=device_data.type,
            description=device_data.description,
            protocol=device_data.protocol,  # Aquí se incluye
        )
        db.add(device)
        await db.flush()  # Necesario para obtener el ID antes de agregar los puertos

        for port_data in device_data.ports:
            port = Port(number=port_data.number, device_id=device.id)
            db.add(port)

        await db.commit()
        await db.refresh(device)
        return device

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Device).options())
        return result.scalars().all()
