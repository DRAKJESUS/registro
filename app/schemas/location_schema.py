from pydantic import BaseModel

class LocationCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True

class LocationOut(LocationCreate):
    id: int

    class Config:
        from_attributes = True