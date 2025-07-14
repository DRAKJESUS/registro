from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.location_model import Location
from ..models.location_history_model import LocationHistory  # ✅ Nuevo modelo de historial
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
        """
        Actualiza nombre y descripción de una localización.
        Guarda en historial si hay cambios.
        """
        location_obj = await db.get(Location, location_id)
        if not location_obj:
            return None

        # Verifica duplicado
        existing = await db.execute(
            select(Location).where(Location.name == location.name, Location.id != location_id)
        )
        if existing.scalar():
            raise ValueError("Ya existe otra localización con ese nombre")

        # Guardar historial si hay cambios
        if location_obj.name != location.name or location_obj.description != location.description:
            history = LocationHistory(
                location_id=location_obj.id,
                action="EDICIÓN DE LOCALIZACIÓN",
                old_name=location_obj.name,
                new_name=location.name,
                old_description=location_obj.description,
                new_description=location.description
            )
            db.add(history)

        # Actualiza datos
        location_obj.name = location.name
        location_obj.description = location.description
        db.add(location_obj)

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
