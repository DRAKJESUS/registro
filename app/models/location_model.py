from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)  # Esta línea asume que agregaste soporte para descripción

    devices = relationship("Device", back_populates="location", cascade="all, delete")
