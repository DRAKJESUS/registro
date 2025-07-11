from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories.history_repository import HistoryRepository

class HistoryService:
    @staticmethod
    async def get_all(db: AsyncSession):
        return await HistoryRepository.get_all(db)
