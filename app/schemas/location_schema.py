from pydantic import BaseModel, Field

class LocationCreate(BaseModel):
    name: str = Field(..., example="Oficina Principal")
    description: str = Field(None, example="Oficinas administrativas del segundo piso")

class LocationOut(LocationCreate):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2
