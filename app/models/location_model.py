from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # Relación con los dispositivos
    devices = relationship(
        "Device",
        back_populates="location",
        cascade="all, delete",
        lazy="selectin"
    )

  
    assignment_history_old = relationship(
        "AssignmentHistory",
        foreign_keys="AssignmentHistory.old_location_id",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    assignment_history_new = relationship(
        "AssignmentHistory",
        foreign_keys="AssignmentHistory.new_location_id",
        lazy="selectin",
        cascade="all, delete-orphan"
    )
