from pydantic import BaseModel
from typing import List

class PortBase(BaseModel):
    port_number: int
    protocol: str  # ✅ Agregado

class PortCreate(PortBase):
    pass

class PortResponse(PortBase):
    id: int
    device_id: int

    class Config:
        orm_mode = True

class DeviceCreate(BaseModel):
    ip: str
    type: str
    description: str
    ports: List[PortCreate]

class DeviceResponse(BaseModel):
    id: int
    ip: str
    type: str
    description: str
    ports: List[PortResponse]

    class Config:
        orm_mode = True
