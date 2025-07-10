from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.assignment_model import AssignmentHistory

class AssignmentService:
    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(AssignmentHistory))
        return result.scalars().all()