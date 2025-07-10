from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, unique=True, index=True)
    type = Column(String)
    description = Column(String)

    ports = relationship("Port", back_populates="device", cascade="all, delete-orphan")


class Port(Base):
    __tablename__ = "ports"

    id = Column(Integer, primary_key=True, index=True)
    port_number = Column(Integer)
    protocol = Column(String)  # ✅ Nuevo campo
    device_id = Column(Integer, ForeignKey("devices.id"))

    device = relationship("Device", back_populates="ports")
