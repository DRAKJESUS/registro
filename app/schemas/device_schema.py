from typing import List, Optional
from pydantic import BaseModel

class PortBase(BaseModel):
    number: int

class PortCreate(PortBase):
    pass

class PortOut(PortBase):
    id: int

    class Config:
        from_attributes = True

class DeviceBase(BaseModel):
    ip: str
    type: str
    description: str
    protocol: str
    location_id: Optional[int] = None

class DeviceCreate(DeviceBase):
    ports: List[PortCreate]

class DeviceOut(DeviceBase):
    id: int
    ports: List[PortOut]

    class Config:
        from_attributes = True
