from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.location_model import Location
from ..schemas.location_schema import LocationCreate

class LocationRepository:
    @staticmethod
    async def create(db: AsyncSession, location_data: LocationCreate):
        location = Location(
            name=location_data.name,
            description=location_data.description
        )
        db.add(location)
        await db.commit()
        await db.refresh(location)
        return location

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Location))
        return result.scalars().all()
