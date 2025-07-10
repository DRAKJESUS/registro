from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from ..models.device_model import Device
from ..schemas.device_schema import DeviceCreate
from ..models.port_model import Port


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
        await db.flush()  # Obtener el ID antes de agregar puertos

        # Añadir puertos si los hay
        for port in device_data.ports:
            db.add(Port(
                number=port.number,
                description=port.description,
                device_id=device.id
            ))

        await db.commit()
        await db.refresh(device)
        return device

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(
            select(Device)
            .options(
                selectinload(Device.ports),
                selectinload(Device.location)
            )
        )
        return result.scalars().all()
