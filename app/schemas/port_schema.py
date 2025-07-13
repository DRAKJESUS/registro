from pydantic import BaseModel
from typing import Optional

class PortCreate(BaseModel):
    port_number: int
    description: str

    class Config:
        from_attributes = True  # compatibilidad con modelos ORM

class PortOut(PortCreate):
    id: int

    class Config:
        from_attributes = True
