from pydantic import BaseModel
from typing import List, Optional


class PortBase(BaseModel):
    number: int

class PortCreate(PortBase):
    pass

class PortOut(PortBase):
    id: int

    class Config:
        from_attributes = True  # Para Pydantic v2

class DeviceBase(BaseModel):
    ip: str
    type: str
    description: Optional[str]
    protocol: str  # Nuevo campo obligatorio

class DeviceCreate(DeviceBase):
    ports: List[PortCreate]

class DeviceOut(DeviceBase):
    id: int
    ports: List[PortOut]
    location_id: Optional[int]

    class Config:
        from_attributes = True
