from fastapi import Depends
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.user_type_model import UserTypeModel


class UserTypeRepository(BaseRepository[UserTypeModel]):
    def __init__(self, db: Session = Depends(get_db)) -> None:
        super().__init__(UserTypeModel, db)

    async def get_by_filter(self, search: str):
        result = await self.db.execute(
            select(self.model).filter(
                or_(
                    self.model.title.like("%" + search + "%"),
                    self.model.value.like("%" + search + "%"),
                )
            )
        )
        return result.scalars().all()

    async def get_by_unique_value(self, value: str, id: int | None = None):
        query = select(self.model).filter(self.model.value == value)
        if id is not None:
            query = query.filter(self.model.id != id)
        result = await self.db.execute(query)
        return result.scalars().first()
