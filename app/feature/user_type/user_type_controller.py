from typing import List, Optional

from fastapi import Depends, Query, Path, APIRouter

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import check_admin
from app.domain.models.user_type_model import UserTypeModel
from app.feature.user_type.dtos.user_type_dto import UserTypeRDTO, UserTypeCDTO
from app.feature.user_type.user_type_repository import UserTypeRepository


class UserTypeController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/", response_model=List[UserTypeRDTO])(self.get_all)
        self.router.post("/create", response_model=UserTypeRDTO)(self.create)
        self.router.get("/get_by_id/{id}", response_model=UserTypeRDTO)(self.get_by_id)
        self.router.put("/update/{id}", response_model=UserTypeRDTO)(self.update)
        self.router.delete("/delete/{id}")(self.delete)

    async def get_all(self, repo: UserTypeRepository = Depends(UserTypeRepository)):
        result = await repo.get_all()
        return result

    async def get_by_id(self, id: int = Path(gt=0), repo: UserTypeRepository = Depends(UserTypeRepository)):
        try:
            result = await repo.get(id=id)
            if result is None:
                raise AppExceptionResponse.not_found(message="Тип пользователя не найден")
            return result
        except Exception as e:
            raise AppExceptionResponse.internal_error(message=str(e))


    async def create(self, UserType_dto: UserTypeCDTO, repo: UserTypeRepository = Depends(UserTypeRepository),current_user=Depends(check_admin)):
        existed_user_type = await repo.get_by_unique_value(value=UserType_dto.value)
        if(existed_user_type is not None):
            raise AppExceptionResponse.bad_request(message="Такое значение для типа пользователя уже существует")
        UserType = UserTypeModel(**UserType_dto.dict())
        result = await repo.create(obj=UserType)
        return result

    async def update(self,UserType_dto: UserTypeCDTO,id: int = Path(gt=0), repo: UserTypeRepository = Depends(UserTypeRepository),current_user=Depends(check_admin)):
        UserType = await repo.get(id=id)
        if UserType is None:
            raise AppExceptionResponse.not_found(message="Тип пользователя не найден")
        existed_UserType = await repo.get_by_unique_value(value=UserType_dto.value,id=id)
        if (existed_UserType is not None):
            raise AppExceptionResponse.bad_request(message="Такое значение для типа пользователя уже существует")
        result = await repo.update(obj=UserType,dto=UserType_dto)
        return result

    async def delete(self, id: int = Path(gt=0), repo: UserTypeRepository = Depends(UserTypeRepository),current_user=Depends(check_admin)):
        await repo.delete(id=id)