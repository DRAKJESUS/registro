from pydantic import BaseModel, Extra

class PortCreate(BaseModel):
    port_number: int
    description: str

    class Config:
        extra = Extra.forbid  # Evita campos no definidos
        from_attributes = True

class PortOut(PortCreate):
    id: int

    class Config:
        from_attributes = True
