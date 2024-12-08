from fastapi import APIRouter, Depends, Path
from sqlalchemy import and_
from sqlalchemy.orm import selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import check_admin, check_admin_and_employee, check_legal_client
from app.core.pagination_dto import PaginationOrganizationRDTOWithRelations
from app.core.validation_rules import TWELVE_DIGITS_REGEX
from app.domain.models.organization_model import OrganizationModel
from app.domain.models.user_model import UserModel
from app.feature.organization.dtos.organization_dto import (
    OrganizationCDTO,
    OrganizationRDTO,
)
from app.feature.organization.filter.organization_filter import OrganizationFilter
from app.feature.organization.organization_repository import OrganizationRepository
from app.feature.organization_type.organization_type_repository import (
    OrganizationTypeRepository,
)
from app.feature.user.user_repository import UserRepository
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import (
    OrganizationRDTOWithRelations,
    UserRDTOWithRelations,
)


class OrganizationController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        (
            self.router.get(
                "/all",
                response_model=PaginationOrganizationRDTOWithRelations,
                summary="Список организаций разделенная по полям пагинации",
                description="Получение списка ролей разделенная по полям пагинации",
            )(self.all)
        )
        self.router.get(
            "/get/{id}",
            response_model=OrganizationRDTOWithRelations,
            summary="Получение организации по уникальному идентификатору",
            description="Получение организации по уникальному идентификатору",
        )(self.get)
        self.router.get(
            "/get-by-bin/{bin}",
            response_model=OrganizationRDTOWithRelations,
            summary="Получение организации по БИНу",
            description="Получение организации по БИНу",
        )(self.get_by_bin)
        self.router.get(
            "/my-organizations",
            response_model=list[OrganizationRDTOWithRelations],
            summary="Получение своих организаций",
            description="Получение своих организаций",
        )(self.my_organizations)
        self.router.post(
            "/create",
            response_model=OrganizationRDTO,
            summary="Создание организации",
            description="Создание организации",
        )(self.create)
        self.router.put(
            "/update/{id}",
            response_model=OrganizationRDTO,
            summary="Обновление организации по уникальному идентификатору",
            description="Обновление организации по уникальному идентификатору",
        )(self.update)
        self.router.put(
            "/delete/{id}",
            summary="Удаление организации по уникальному идентификатору",
            description="Удаление организации по уникальному идентификатору",
        )(self.delete)

    async def all(
        self,
        params: OrganizationFilter = Depends(),
        repo: OrganizationRepository = Depends(OrganizationRepository),
        current_user=Depends(check_admin),
    ):
        result = await repo.paginate_with_filter(
            dto=OrganizationRDTOWithRelations,
            page=params.page,
            per_page=params.per_page,
            filters=params.apply(),
            options=[
                selectinload(OrganizationModel.owner),
                selectinload(OrganizationModel.type),
            ],
        )
        return result

    async def my_organizations(
        self,
        repo: OrganizationRepository = Depends(OrganizationRepository),
        userRDTO: UserRDTOWithRelations = Depends(check_legal_client),
    ):
        return await repo.get_all_with_filter(
            filters=[and_(repo.model.owner_id == userRDTO.id)],
            options=[selectinload(repo.model.owner), selectinload(repo.model.type)],
        )

    async def get(
        self,
        id: int = Path(gt=0),
        repo: OrganizationRepository = Depends(OrganizationRepository),
        current_user=Depends(check_admin_and_employee),
    ):
        result = await repo.get(
            id=id,
            options=[
                selectinload(OrganizationModel.owner),
                selectinload(OrganizationModel.type),
            ],
        )
        if result is None:
            raise AppExceptionResponse.not_found(message="Организация не найдена")
        return result

    async def get_by_bin(
        self,
        bin: str = Path(regex=TWELVE_DIGITS_REGEX, title="БИН", example="000000000000"),
        repo: OrganizationRepository = Depends(OrganizationRepository),
        current_user=Depends(check_admin_and_employee),
    ):
        existed_by_bin = await repo.get_filtered(
            {"bin": bin},
            options=[
                selectinload(OrganizationModel.owner),
                selectinload(OrganizationModel.type),
            ],
        )
        if existed_by_bin is None:
            raise AppExceptionResponse.not_found(message="Организация не найдена")
        return existed_by_bin

    async def create(
        self,
        organization_dto: OrganizationCDTO,
        repo: OrganizationRepository = Depends(OrganizationRepository),
        userRepo: UserRepository = Depends(UserRepository),
        organizationTypeRepository=Depends(OrganizationTypeRepository),
        current_user=Depends(check_admin),
    ):
        await self.check_form(
            dto=organization_dto,
            repo=repo,
            userRepo=userRepo,
            organizationTypeRepository=organizationTypeRepository,
        )
        result = await repo.create(OrganizationModel(**organization_dto.dict()))
        return result

    async def update(
        self,
        organization_dto: OrganizationCDTO,
        id: int = Path(gt=0),
        repo: OrganizationRepository = Depends(OrganizationRepository),
        userRepo: UserRepository = Depends(UserRepository),
        organizationTypeRepostitory=Depends(OrganizationTypeRepository),
        current_user=Depends(check_admin),
    ):
        organization = await repo.get(id)
        if organization is None:
            raise AppExceptionResponse.not_found(message="Организация не найдена")
        await self.check_form(
            dto=organization_dto,
            repo=repo,
            userRepo=userRepo,
            organizationTypeRepository=organizationTypeRepostitory,
            id=id,
        )
        result = await repo.update(obj=organization, dto=organization_dto)
        return result

    async def delete(
        self,
        id: int = Path(gt=0),
        repo: OrganizationRepository = Depends(OrganizationRepository),
        current_user=Depends(check_admin),
    ) -> None:
        await repo.delete(id=id)

    @staticmethod
    async def check_form(
        dto: OrganizationCDTO,
        repo: OrganizationRepository,
        userRepo: UserRepository,
        organizationTypeRepository: OrganizationTypeRepository,
        id: int | None = None,
    ) -> None:
        existed_by_bin = await repo.get_filtered({"bin": dto.bin})
        if existed_by_bin is not None and existed_by_bin.id != id:
            raise AppExceptionResponse.bad_request(message="Такой БИН уже существует")

        existed_by_bik = await repo.get_filtered({"bik": dto.bik})
        if existed_by_bik is not None and existed_by_bik.id != id:
            raise AppExceptionResponse.bad_request(message="Такой БИК уже существует")

        existed_by_email = await repo.get_filtered({"email": dto.email})
        if existed_by_email is not None and existed_by_email.id != id:
            raise AppExceptionResponse.bad_request(message="Такая почта уже существует")

        existed_by_phone = await repo.get_filtered({"phone": dto.phone})
        if existed_by_phone is not None and existed_by_phone.id != id:
            raise AppExceptionResponse.bad_request(message="Такой телефон уже существует")

        organizationType = await organizationTypeRepository.get(id=dto.type_id)
        if organizationType is None:
            raise AppExceptionResponse.bad_request(
                message="Такого типа юридического лица не существует"
            )

        owner = await userRepo.get(
            id=dto.owner_id, options=[selectinload(UserModel.user_type)]
        )
        if owner is None:
            raise AppExceptionResponse.bad_request(message="Такого пользователя нет")
        if owner.user_type.value != TableConstantsNames.UserLegalTypeValue:
            raise AppExceptionResponse.bad_request(
                message="Пользователь должен быть юридическим лицом"
            )
