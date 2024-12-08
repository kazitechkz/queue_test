from fastapi import APIRouter, Depends, Path

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import check_admin, get_current_user
from app.domain.models.user_type_model import UserTypeModel
from app.feature.user_type.dtos.user_type_dto import UserTypeCDTO, UserTypeRDTO
from app.feature.user_type.user_type_repository import UserTypeRepository


class UserTypeController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            "/",
            response_model=list[UserTypeRDTO],
            summary="Получение типа пользователей",
            description="Тип пользователя - физ.лицо или юр.лицо",
        )(self.get_all)
        (
            self.router.post(
                "/create",
                response_model=UserTypeRDTO,
                summary="Создание типа пользователя",
                description="Создание типа пользователя",
            )(self.create)
        )
        self.router.get(
            "/get-by-id/{id}",
            response_model=UserTypeRDTO,
            summary="Получение типа пользователя",
            description="Получение типа пользователя по идентификатору",
        )(self.get_by_id)
        self.router.put(
            "/update/{id}",
            response_model=UserTypeRDTO,
            summary="Обновление типа пользователя по уникальному идентификатору",
            description="Обновление типа пользователя по идентификатору",
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            summary="Удаление типа пользователя по уникальному идентификатору",
            description="Удаление типа пользователя по идентификатору",
        )(self.delete)

    async def get_all(self, repo: UserTypeRepository = Depends(UserTypeRepository)):
        result = await repo.get_all()
        return result

    async def get_by_id(
        self,
        id: int = Path(gt=0),
        repo: UserTypeRepository = Depends(UserTypeRepository),
        current_user=Depends(get_current_user),
    ):
        try:
            result = await repo.get(id=id)
            if result is None:
                raise AppExceptionResponse.not_found(message="Тип пользователя не найден")
            return result
        except Exception as e:
            raise AppExceptionResponse.internal_error(message=str(e))

    async def create(
        self,
        UserType_dto: UserTypeCDTO,
        repo: UserTypeRepository = Depends(UserTypeRepository),
        current_user=Depends(check_admin),
    ):
        existed_user_type = await repo.get_by_unique_value(value=UserType_dto.value)
        if existed_user_type is not None:
            raise AppExceptionResponse.bad_request(
                message="Такое значение для типа пользователя уже существует"
            )
        UserType = UserTypeModel(**UserType_dto.dict())
        result = await repo.create(obj=UserType)
        return result

    async def update(
        self,
        UserType_dto: UserTypeCDTO,
        id: int = Path(gt=0),
        repo: UserTypeRepository = Depends(UserTypeRepository),
        current_user=Depends(check_admin),
    ):
        UserType = await repo.get(id=id)
        if UserType is None:
            raise AppExceptionResponse.not_found(message="Тип пользователя не найден")
        existed_UserType = await repo.get_by_unique_value(value=UserType_dto.value, id=id)
        if existed_UserType is not None:
            raise AppExceptionResponse.bad_request(
                message="Такое значение для типа пользователя уже существует"
            )
        result = await repo.update(obj=UserType, dto=UserType_dto)
        return result

    async def delete(
        self,
        id: int = Path(gt=0),
        repo: UserTypeRepository = Depends(UserTypeRepository),
        current_user=Depends(check_admin),
    ) -> None:
        await repo.delete(id=id)
