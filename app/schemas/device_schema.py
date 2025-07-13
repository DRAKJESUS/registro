from pydantic import BaseModel
from typing import List, Optional
from .port_schema import PortCreate, PortOut
from .location_schema import LocationOut

class DeviceCreate(BaseModel):
    ip: str
    status: str
    description: str
    protocol: str
    location_id: Optional[int]
    ports: List[PortCreate]  # ✅ Importante: usar PortCreate, NO PortOut

    class Config:
        from_attributes = True

class DeviceUpdate(BaseModel):
    ip: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    protocol: Optional[str] = None
    location_id: Optional[int] = None
    ports: Optional[List[PortCreate]] = None  # ✅ También usar PortCreate aquí

    class Config:
        from_attributes = True

class DeviceOut(BaseModel):
    id: int
    ip: str
    status: str
    description: str
    protocol: str
    location: Optional[LocationOut]
    ports: List[PortOut]  # ✅ Mostrar los puertos con ID

    class Config:
        from_attributes = True
