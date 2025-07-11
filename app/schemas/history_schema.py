from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HistoryOut(BaseModel):
    id: int
    device_id: int
    action: str
    old_location_id: Optional[int] = None
    new_location_id: Optional[int] = None
    old_status: Optional[str] = None
    new_status: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True  # Pydantic v2
