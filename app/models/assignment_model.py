from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..database import Base

class AssignmentHistory(Base):
    __tablename__ = "assignment_history"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id", ondelete="CASCADE"), nullable=False)

    action = Column(String, nullable=False)  # Ej: CAMBIO DE STATUS, CAMBIO DE LOCALIZACIÓN, ASIGNACIÓN DE LOCALIZACIÓN

    old_status = Column(String, nullable=True)
    new_status = Column(String, nullable=True)

    old_location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True)
    new_location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones opcionales para acceder a datos del dispositivo o ubicación si lo necesitas
    device = relationship("Device", back_populates="history", lazy="joined")
