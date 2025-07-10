from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from ..models.device_model import Device
from ..models.port_model import Port
from ..schemas.device_schema import DeviceCreate

class DeviceRepository:

    @staticmethod
    async def create(db: AsyncSession, device: DeviceCreate):
        new_device = Device(
            ip=device.ip,
            type=device.type,
            description=device.description,
            protocol=device.protocol
        )
        db.add(new_device)
        await db.flush()  # Para obtener new_device.id sin commit aún

        for port in device.ports:
            db.add(Port(number=port.number, device_id=new_device.id))

        await db.commit()
        await db.refresh(new_device)
        return new_device

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(
            select(Device).options(selectinload(Device.ports))
        )
        return result.scalars().all()
