from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, unique=True, index=True)
    status = Column(String)  # Ejemplo: "activo", "inactivo"
    description = Column(String)
    protocol = Column(String)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)

    ports = relationship(
        "Port",
        back_populates="device",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    location = relationship(
        "Location",
        back_populates="devices",
        lazy="joined"
    )

    history = relationship(
        "AssignmentHistory",
        back_populates="device",
        lazy="selectin",
        cascade="all, delete-orphan"
    )
