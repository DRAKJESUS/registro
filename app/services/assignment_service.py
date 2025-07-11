from sqlalchemy.ext.asyncio import AsyncSession
from ..models.assignment_model import AssignmentHistory
from sqlalchemy.future import select

class AssignmentService:
    @staticmethod
    async def get_all_history(db: AsyncSession):
        result = await db.execute(select(AssignmentHistory))
        return result.scalars().all()
