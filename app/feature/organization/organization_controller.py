import logging
from typing import Optional

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import selectinload
from app.core.app_exception_response import AppExceptionResponse
from app.core.validation_rules import TWELVE_DIGITS_REGEX
from app.domain.models.organization_model import OrganizationModel
from app.domain.models.user_model import UserModel
from app.feature.organization.dtos.organization_dto import OrganizationRDTO, OrganizationCDTO
from app.feature.organization.filter.organization_filter import OrganizationFilter
from app.feature.organization.organization_repository import OrganizationRepository
from app.feature.organization_type.organization_type_repository import OrganizationTypeRepository
from app.feature.user.user_repository import UserRepository
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import OrganizationRDTOWithRelations


class OrganizationController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/all")(self.all)
        self.router.get("/get/{id}", response_model=OrganizationRDTOWithRelations)(self.get)
        self.router.get("/get_by_bin/{bin}", response_model=OrganizationRDTOWithRelations)(self.get_by_bin)
        self.router.post("/create", response_model=OrganizationRDTO)(self.create)
        self.router.put("/update/{id}", response_model=OrganizationRDTO)(self.update)
        self.router.put("/delete/{id}")(self.delete)

    async def all(self,
                  params: OrganizationFilter = Depends(),
                  repo: OrganizationRepository = Depends(OrganizationRepository)):
        result = await repo.paginate_with_filter(
            dto=OrganizationRDTOWithRelations, page=params.page,
            per_page=params.per_page, filters=params.apply(),
            options=[selectinload(OrganizationModel.owner),selectinload(OrganizationModel.type)])
        return result

    async def get(self, id: int = Path(gt=0), repo: OrganizationRepository = Depends(OrganizationRepository)):
        result = await repo.get(id=id, options=[selectinload(OrganizationModel.owner),selectinload(OrganizationModel.type)])
        if result is None:
            raise AppExceptionResponse.not_found(message="Организация не найдена")
        return result

    async def get_by_bin(self, bin: str = Path(regex=TWELVE_DIGITS_REGEX, title='БИН', example="000000000000"),
                         repo: OrganizationRepository = Depends(OrganizationRepository)):
        existed_by_bin = await repo.get_filtered({"bin": bin}, options=[selectinload(OrganizationModel.owner),selectinload(OrganizationModel.type)])
        if existed_by_bin is None:
            raise AppExceptionResponse.not_found(message="Организация не найдена")
        return existed_by_bin

    async def create(self,
                     organization_dto: OrganizationCDTO,
                     repo: OrganizationRepository = Depends(OrganizationRepository),
                     userRepo: UserRepository = Depends(UserRepository),
                     organizationTypeRepository=Depends(OrganizationTypeRepository)
                     ):
        await self.check_form(dto=organization_dto, repo=repo, userRepo=userRepo,
                              organizationTypeRepository=organizationTypeRepository)
        result = await repo.create(OrganizationModel(**organization_dto.dict()))
        return result

    async def update(self,
                     organization_dto: OrganizationCDTO,
                     id: int = Path(gt=0),
                     repo: OrganizationRepository = Depends(OrganizationRepository),
                     userRepo: UserRepository = Depends(UserRepository),
                     organizationTypeRepostitory=Depends(OrganizationTypeRepository)
                     ):
        organization = await repo.get(id)
        if organization is None:
            raise AppExceptionResponse.not_found(message="Организация не найдена")
        await self.check_form(dto=organization_dto, repo=repo, userRepo=userRepo,
                              organizationTypeRepository=organizationTypeRepostitory, id=id)
        result = await repo.update(obj=organization, dto=organization_dto)
        return result

    async def delete(self, id: int = Path(gt=0), repo: OrganizationRepository = Depends(OrganizationRepository)):
        await repo.delete(id=id)

    @staticmethod
    async def check_form(
            dto: OrganizationCDTO,
            repo: OrganizationRepository,
            userRepo: UserRepository,
            organizationTypeRepository: OrganizationTypeRepository,
            id: Optional[int] = None):
        existed_by_bin = await repo.get_filtered({"bin": dto.bin})
        if existed_by_bin is not None:
            if existed_by_bin.id != id:
                raise AppExceptionResponse.bad_request(message="Такой БИН уже существует")

        existed_by_bik = await repo.get_filtered({"bik": dto.bik})
        if existed_by_bik is not None:
            if existed_by_bik.id != id:
                raise AppExceptionResponse.bad_request(message="Такой БИК уже существует")

        existed_by_email = await repo.get_filtered({"email": dto.email})
        if existed_by_email is not None:
            if existed_by_email.id != id:
                raise AppExceptionResponse.bad_request(message="Такая почта уже существует")

        existed_by_phone = await repo.get_filtered({"phone": dto.phone})
        if existed_by_phone is not None:
            if existed_by_phone.id != id:
                raise AppExceptionResponse.bad_request(message="Такой телефон уже существует")

        organizationType = await organizationTypeRepository.get(id=dto.type_id)
        if organizationType is None:
            raise AppExceptionResponse.bad_request(message="Такого типа юридического лица не существует")

        owner = await userRepo.get(id=dto.owner_id,options=[selectinload(UserModel.user_type)])
        if owner is None:
            raise AppExceptionResponse.bad_request(message="Такого пользователя нет")
        else:
            if owner.user_type.value != TableConstantsNames.UserLegalTypeValue:
                raise AppExceptionResponse.bad_request(message="Пользователь должен быть юридическим лицом")
