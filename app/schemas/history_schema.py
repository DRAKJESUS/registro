from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AssignmentHistoryOut(BaseModel):
    id: int
    device_id: int
    action: str
    old_status: Optional[str]
    new_status: Optional[str]
    old_location_id: Optional[int]
    new_location_id: Optional[int]
    timestamp: datetime

    class Config:
        from_attributes = True  # o orm_mode = True si usas Pydantic v1
