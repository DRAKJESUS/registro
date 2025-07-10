from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from ..database import Base

class AssignmentHistory(Base):
    __tablename__ = "assignment_history"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, nullable=False)
    old_location_id = Column(Integer, nullable=True)
    new_location_id = Column(Integer, nullable=True)
    action = Column(String)  # ASSIGNED | UNASSIGNED | MOVED
    timestamp = Column(DateTime(timezone=True), server_default=func.now())