from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from ..database import Base

class AssignmentHistory(Base):
    __tablename__ = "assignment_history"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    action = Column(String)
    old_location_id = Column(Integer, nullable=True)
    new_location_id = Column(Integer, nullable=True)
    old_status = Column(String, nullable=True)
    new_status = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
