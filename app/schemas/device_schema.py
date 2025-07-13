from pydantic import BaseModel
from typing import List, Optional
from .port_schema import PortCreate, PortOut

class DeviceCreate(BaseModel):
    ip: str
    status: str
    description: str
    protocol: str
    location_id: Optional[int]
    ports: List[PortCreate]

    class Config:
        from_attributes = True

class DeviceOut(BaseModel):
    id: int
    ip: str
    status: str
    description: str
    protocol: str
    location_id: Optional[int]
    ports: List[PortOut]

    class Config:
        from_attributes = True

class DeviceUpdate(BaseModel):
    ip: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    protocol: Optional[str] = None
    location_id: Optional[int] = None
    ports: Optional[List[PortCreate]] = None

    class Config:
        from_attributes = True
