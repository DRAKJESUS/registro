from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AssignmentOut(BaseModel):
    id: int
    device_id: int
    action: str
    old_location_id: Optional[int]
    new_location_id: Optional[int]
    old_status: Optional[str]
    new_status: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True
