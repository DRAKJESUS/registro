from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    protocol = Column(String, nullable=False)  # Nuevo campo
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)

    location = relationship("Location", back_populates="devices")
    ports = relationship("Port", back_populates="device", cascade="all, delete-orphan")


class Port(Base):
    __tablename__ = "ports"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    number = Column(Integer, nullable=False)

    device = relationship("Device", back_populates="ports")
