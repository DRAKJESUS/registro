from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from ..models.device_model import Device
from ..models.port_model import Port
from ..schemas.device_schema import DeviceCreate

class DeviceRepository:
    @staticmethod
    async def create(db: AsyncSession, device_data: DeviceCreate):
        device = Device(
            ip=device_data.ip,
            status=device_data.status,  # CAMBIO
            description=device_data.description,
            protocol=device_data.protocol,
            location_id=device_data.location_id
        )
        db.add(device)
        await db.flush()

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
        result = await db.execute(
            select(Device).options(selectinload(Device.ports))
        )
        return result.scalars().all()
