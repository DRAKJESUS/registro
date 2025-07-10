from pydantic import BaseModel
from typing import List, Optional
from .port_schema import PortCreate, PortOut

class DeviceCreate(BaseModel):
    ip: str
    type: str
    description: str
    protocol: str
    ports: List[PortCreate]
    location_id: Optional[int] = None

class DeviceOut(DeviceCreate):
    id: int
    ports: List[PortOut]

    class Config:
        orm_mode = True
