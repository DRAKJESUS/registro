from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import logging

from ..models.assignment_model import AssignmentHistory

logger = logging.getLogger(__name__)

class HistoryService:
    @staticmethod
    async def get_all(db: AsyncSession) -> List[AssignmentHistory]:
        try:
            result = await db.execute(select(AssignmentHistory).order_by(AssignmentHistory.timestamp.desc()))
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error al obtener historial: {e}")
            raise
