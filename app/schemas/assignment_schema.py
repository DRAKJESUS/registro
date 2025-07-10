from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AssignmentOut(BaseModel):
    id: int
    device_id: int
    old_location_id: Optional[int]
    new_location_id: Optional[int]
    action: str
    timestamp: datetime

    class Config:
        from_attributes = True