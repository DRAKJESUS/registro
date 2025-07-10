from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.location_schema import LocationCreate
from ..repositories.location_repository import LocationRepository

class LocationService:
    @staticmethod
    async def create(db: AsyncSession, location: LocationCreate):
        return await LocationRepository.create(db, location)

    @staticmethod
    async def get_all(db: AsyncSession):
        return await LocationRepository.get_all(db)
