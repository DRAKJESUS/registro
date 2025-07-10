from ..models.device_model import Device, Port
from ..schemas.device_schema import DeviceCreate

async def create_device(db: AsyncSession, device: DeviceCreate):
    db_device = Device(
        ip=device.ip,
        type=device.type,
        description=device.description
    )
    db_device.ports = [
        Port(port_number=p.port_number, protocol=p.protocol)
        for p in device.ports
    ]
    db.add(db_device)
    await db.commit()
    await db.refresh(db_device)
    return db_device
