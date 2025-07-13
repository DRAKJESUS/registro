from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.location_model import Location
from ..schemas.location_schema import LocationCreate

class LocationService:
    @staticmethod
    async def create(db: AsyncSession, location: LocationCreate) -> Location:
        existing = await db.execute(select(Location).where(Location.name == location.name))
        if existing.scalar():
            raise ValueError("Ya existe una localización con ese nombre")

        new_loc = Location(name=location.name, description=location.description)
        db.add(new_loc)
        await db.commit()
        await db.refresh(new_loc)
        return new_loc

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Location))
        return result.scalars().all()

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str):
        result = await db.execute(select(Location).where(Location.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def get(db: AsyncSession, location_id: int):
        return await db.get(Location, location_id)

    @staticmethod
    async def update(db: AsyncSession, location_id: int, location: LocationCreate):
        location_obj = await db.get(Location, location_id)
        if not location_obj:
            return None

        # Verifica si ya existe otra localización con ese nombre (distinto ID)
        existing = await db.execute(
            select(Location).where(Location.name == location.name, Location.id != location_id)
        )
        if existing.scalar():
            raise ValueError("Ya existe otra localización con ese nombre")

        location_obj.name = location.name
        location_obj.description = location.description
        await db.commit()
        await db.refresh(location_obj)
        return location_obj

    @staticmethod
    async def delete(db: AsyncSession, location_id: int):
        location = await db.get(Location, location_id)
        if not location:
            return False
        await db.delete(location)
        await db.commit()
        return True
