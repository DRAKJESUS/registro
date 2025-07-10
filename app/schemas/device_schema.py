from pydantic import BaseModel, Field
from typing import List

class PortSchema(BaseModel):
    number: int = Field(..., description="Número de puerto asociado al dispositivo")

    class Config:
        from_attributes = True

class DeviceCreate(BaseModel):
    ip: str = Field(..., description="Dirección IP del dispositivo")
    type: str = Field(..., description="Tipo de dispositivo (ej. Cámara, Sensor, etc.)")
    description: str = Field(..., description="Descripción breve del dispositivo")
    ports: List[PortSchema] = Field(..., description="Lista de puertos asociados")

class DeviceOut(DeviceCreate):
    id: int
    ports: List[PortSchema]

    class Config:
        from_attributes = True