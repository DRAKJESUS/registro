from pydantic import BaseModel
from typing import List, Optional
from .port_schema import PortCreate, PortOut

class DeviceCreate(BaseModel):
    ip: str
    status: str  # CAMBIO
    description: str
    protocol: str
    location_id: Optional[int]
    ports: List[PortCreate]

    class Config:
        from_attributes = True

class DeviceOut(BaseModel):
    id: int
    ip: str
    status: str  # CAMBIO
    description: str
    protocol: str
    location_id: Optional[int]
    ports: List[PortOut]

    class Config:
        from_attributes = True

class DeviceUpdate(BaseModel):
    ip: Optional[str]
    status: Optional[str]
    description: Optional[str]
    protocol: Optional[str]
    location_id: Optional[int]
    ports: Optional[List[PortCreate]]

    class Config:
        from_attributes = True
