from pydantic import BaseModel

class PortCreate(BaseModel):
    port_number: int
    description: str

class PortOut(PortCreate):
    id: int

    class Config:
        orm_mode = True
