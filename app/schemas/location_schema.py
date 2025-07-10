from pydantic import BaseModel

class LocationCreate(BaseModel):
    name: str
    description: str

class LocationOut(LocationCreate):
    id: int

    class Config:
        orm_mode = True
