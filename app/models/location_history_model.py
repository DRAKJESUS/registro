from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from ..database import Base

class LocationHistory(Base):
    __tablename__ = "location_history"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)

    action = Column(String, nullable=False)  # Ej: EDICIÓN DE LOCALIZACIÓN

    old_name = Column(String, nullable=True)
    new_name = Column(String, nullable=True)

    old_description = Column(String, nullable=True)
    new_description = Column(String, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())
