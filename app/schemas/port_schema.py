from pydantic import BaseModel, Extra

class PortCreate(BaseModel):
    port_number: int
    description: str

    class Config:
        extra = Extra.forbid  # ❌ Prohíbe campos no declarados

class PortOut(PortCreate):
    id: int

    class Config:
        orm_mode = True
