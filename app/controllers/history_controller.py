from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..schemas.history_schema import HistoryOut
from ..services.history_service import HistoryService
from ..database import get_session

router = APIRouter(prefix="/history", tags=["Historial"])

@router.get("/", response_model=List[AssignmentHistoryOut])
async def get_history(db: AsyncSession = Depends(get_session)):
    return await AssignmentHistoryService.get_all(db)
