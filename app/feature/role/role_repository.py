from typing import Optional

from fastapi import Depends
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.role_model import RoleModel


class RoleRepository(BaseRepository[RoleModel]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(RoleModel, db)

    async def get_by_filter(self, search: str):
        result = await self.db.execute(select(self.model).filter(
            or_(self.model.title.like("%" + search + "%"), self.model.value.like("%" + search + "%"), )))
        return result.scalars().all()

    async def get_by_unique_value(self, value: str, id: Optional[int] = None):
        query = select(self.model).filter(self.model.value == value)
        if id is not None:
            query = query.filter(self.model.id != id)
        result = await self.db.execute(query)
        return result.scalars().first()
