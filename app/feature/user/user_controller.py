from typing import Optional

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import get_password_hash, check_admin, check_admin_and_employee, get_current_user
from app.core.pagination_dto import Pagination, PaginationUserRDTOWithRelations
from app.core.validation_rules import TWELVE_DIGITS_REGEX, EMAIL_REGEX, PHONE_REGEX
from app.domain.models.user_model import UserModel
from app.feature.role.role_repository import RoleRepository
from app.feature.user.dtos.user_dto import UserCDTO, UserRDTO
from app.feature.user.filter.user_filter import UserFilter
from app.feature.user.user_repository import UserRepository
from app.feature.user_type.user_type_repository import UserTypeRepository
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class UserController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        (self.router.post(
            "/create",
            response_model=UserRDTO,
            summary="Создание пользователя",
            description="Создание пользователя"
        )
         (self.create))
        self.router.put(
            "/update/{id}",
            response_model=UserRDTO,
            summary="Обновление пользователя по уникальному идентификатору",
            description="Обновление пользователя по уникальному идентификатору"
        )(self.update)
        self.router.get(
            "/all",
            response_model=PaginationUserRDTOWithRelations,
            summary="Получение списка пользоватей по параметрам пагинации",
            description="Получение списка пользоватей по параметрам пагинации"
        )(self.all)
        self.router.get(
            "/get/{id}",
            response_model=UserRDTOWithRelations,
            summary="Получение пользователя по уникальному идентификатору",
            description="Получение пользователя по уникальному идентификатору"
        )(self.get)
        self.router.get(
            "/get-by-iin/{iin}",
            response_model=UserRDTOWithRelations,
            summary="Получение пользователя по ИИНу",
            description="Получение пользователя по ИИНу"
        )(self.get_by_iin)
        self.router.get(
            "/get-by-email/{email}",
            response_model=UserRDTOWithRelations,
            summary="Получение пользователя по почте",
            description="Получение пользователя по почте"
        )(self.get_by_email)
        self.router.get(
            "/get-by-phone/{phone}",
            response_model=UserRDTOWithRelations,
            summary="Получение пользователя по телефону",
            description="Получение пользователя по телефону"
        )(self.get_by_phone)
        self.router.delete(
            "/delete/{id}",
            summary="Удаление пользователя по уникальному идентификатору",
            description="Удаление пользователя по уникальному идентификатору"
        )(self.delete)

    async def create(self, user_dto: UserCDTO, repo: UserRepository = Depends(UserRepository),
                     repoRole: RoleRepository = Depends(RoleRepository),
                     userTypeRepo: UserTypeRepository = Depends(UserTypeRepository),
                     current_user=Depends(check_admin)
                     ):
        await self.check_form(repo, repoRole, userTypeRepo, user_dto)
        user_dto.password_hash = get_password_hash(user_dto.password_hash)
        result = await repo.create(UserModel(**user_dto.dict()))
        return result

    async def update(self, user_dto: UserCDTO, id: int = Path(gt=0), repo: UserRepository = Depends(UserRepository),
                     repoRole: RoleRepository = Depends(RoleRepository),
                     userTypeRepo: UserTypeRepository = Depends(UserTypeRepository),
                     current_user=Depends(check_admin)
                     ):
        user = await repo.get(id)
        if user is None:
            raise AppExceptionResponse.not_found(message="Пользователь не найден")
        await self.check_form(repo, repoRole, userTypeRepo, user_dto, id)
        user_dto.password_hash = get_password_hash(user_dto.password_hash)
        result = await repo.update(obj=user, dto=user_dto)
        return result

    async def get(
            self,
            id: int = Path(gt=0),
            repo: UserRepository = Depends(UserRepository),
            current_user=Depends(check_admin_and_employee),
    ):
        result = await repo.get(id=id, options=[
                selectinload(UserModel.role),
                selectinload(UserModel.user_type),
                selectinload(UserModel.organizations)
        ])
        if result is None:
            raise AppExceptionResponse.not_found(message="Пользователь не найден")
        return result

    async def all(self,
                  params: UserFilter = Depends(),
                  repo: UserRepository = Depends(UserRepository),
                  current_user=Depends(check_admin)):
        result = await repo.paginate_with_filter(dto=UserRDTOWithRelations, page=params.page, per_page=params.per_page,
                                                 filters=params.apply(), options=[selectinload(UserModel.role),
                                                                                  selectinload(UserModel.user_type),
                                                                                  selectinload(UserModel.organizations),
                                                                                  ])
        return result

    async def get_by_iin(
            self,
            iin: str = Path(regex=TWELVE_DIGITS_REGEX, title='ИИН',example="XXXXXXXXXXXX"),
            repo: UserRepository = Depends(UserRepository),
            current_user=Depends(check_admin_and_employee),
    ):
        user_iin = await repo.get_filtered({"iin": iin},
                                           options=[selectinload(UserModel.role), selectinload(UserModel.user_type),
                                                    selectinload(UserModel.organizations), ])
        if user_iin is None:
            raise AppExceptionResponse.not_found(message="Пользователь не найден")
        return user_iin

    async def get_by_email(
            self,
            email: str = Path(regex=EMAIL_REGEX, title='Почта',example="example@gmail.com"),
            repo: UserRepository = Depends(UserRepository),
            current_user=Depends(check_admin_and_employee),
    ):
        user_email = await repo.get_filtered({"email": email},
                                             options=[selectinload(UserModel.role), selectinload(UserModel.user_type),
                                                      selectinload(UserModel.organizations), ])
        if user_email is None:
            raise AppExceptionResponse.not_found(message="Пользователь не найден")
        return user_email

    async def get_by_phone(
            self,
            phone: str = Path(regex=PHONE_REGEX, title='Телефон', example="+77XXXXXXX"),
            repo: UserRepository = Depends(UserRepository),
            current_user=Depends(check_admin_and_employee),
    ):
        user_phone = await repo.get_filtered({"phone": phone},
                                             options=[selectinload(UserModel.role), selectinload(UserModel.user_type),
                                                      selectinload(UserModel.organizations), ])
        if user_phone is None:
            raise AppExceptionResponse.not_found(message="Пользователь не найден")
        return user_phone

    async def delete(
            self,
            id: int = Path(gt=0),
            repo: UserRepository = Depends(UserRepository),
            current_user=Depends(check_admin),
    ):
        await repo.delete(id=id)

    @staticmethod
    async def check_form(repo: UserRepository, repoRole: RoleRepository, userTypeRepo: UserTypeRepository,
                         user_dto: UserCDTO, id: Optional[int] = None):
        user_email = await repo.get_filtered({"email": user_dto.email})

        if user_email is not None:
            if user_email.id != id:
                raise AppExceptionResponse.bad_request(message="Такая почта уже существует")

        user_phone = await repo.get_filtered({"phone": user_dto.phone})
        if user_phone is not None:
            if user_phone.id != id:
                raise AppExceptionResponse.bad_request(message="Такой телефон уже существует")

        user_iin = await repo.get_filtered({"iin": user_dto.iin})
        if user_iin is not None:
            if user_iin.id != id:
                raise AppExceptionResponse.bad_request(message="Такой иин уже существует")

        role_id = await repoRole.get(id=user_dto.role_id)
        if role_id is None:
            raise AppExceptionResponse.bad_request(message="Роли не существует")

        type_id = await userTypeRepo.get(id=user_dto.type_id)
        if type_id is None:
            raise AppExceptionResponse.bad_request(message="Такого типа не существует")
