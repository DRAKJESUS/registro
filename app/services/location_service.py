from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.location_schema import LocationCreate
from ..models.location_model import Location
from sqlalchemy.future import select

class LocationService:
    @staticmethod
    async def create(db: AsyncSession, loc: LocationCreate):
        location = Location(name=loc.name)
        db.add(location)
        await db.commit()
        await db.refresh(location)
        return location

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Location))
        return result.scalars().all()