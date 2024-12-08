from fastapi import Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session, selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.user_model import UserModel
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, db: Session = Depends(get_db)) -> None:
        super().__init__(UserModel, db)

    async def get_admin(self) -> UserRDTOWithRelations:
        result = await self.get_with_filter(
            filters=[and_(self.model.role_id == TableConstantsNames.RoleAdminId)],
            options=[
                selectinload(self.model.role),
                selectinload(self.model.user_type),
                selectinload(self.model.organizations),
            ],
        )
        if result is None:
            raise AppExceptionResponse.internal_error(message="Система не найдена")
        return UserRDTOWithRelations.from_orm(result)
