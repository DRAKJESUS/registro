from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Port(Base):
    __tablename__ = "ports"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    device_id = Column(Integer, ForeignKey("devices.id"))

    device = relationship("Device", back_populates="ports")
