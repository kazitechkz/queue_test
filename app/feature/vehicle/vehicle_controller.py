from typing import List, Optional

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.domain.models.vehicle_model import VehicleModel
from app.feature.organization.organization_repository import OrganizationRepository
from app.feature.region.region_repository import RegionRepository
from app.feature.user.user_repository import UserRepository
from app.feature.vehicle.dtos.vehicle_dto import VehicleRDTO, VehicleWithRelationsDTO, VehicleCDTO
from app.feature.vehicle.filter.vehicle_filter import VehicleFilter
from app.feature.vehicle.vehicle_repository import VehicleRepository
from app.feature.vehicle_category.vehicle_category_repository import VehicleCategoryRepository
from app.feature.vehicle_color.vehicle_color_repository import VehicleColorRepository


class VehicleController:

    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/",)(self.all)
        self.router.post("/create", response_model=VehicleRDTO)(self.create)
        self.router.get("/get/{id}", response_model=VehicleWithRelationsDTO)(self.get)
        self.router.put("/update/{id}", response_model=VehicleRDTO)(self.update)
        self.router.delete("/delete/{id}")(self.delete)

    async def all(self,params:VehicleFilter = Depends(),
                  repo: VehicleRepository = Depends(VehicleRepository)
                  ):
        result = await repo.paginate_with_filter(dto=VehicleWithRelationsDTO,page=params.page,per_page=params.per_page,filters=params.apply(),options=[
            selectinload(VehicleModel.category),
            selectinload(VehicleModel.color),
            selectinload(VehicleModel.region),
            selectinload(VehicleModel.owner),
            selectinload(VehicleModel.organization),
        ])
        return result


    async def get(self, id: int = Path(gt=0), repo: VehicleRepository = Depends(VehicleRepository)):
        result = await repo.get(id=id, options=[
            selectinload(VehicleModel.category),
            selectinload(VehicleModel.color),
            selectinload(VehicleModel.region),
            selectinload(VehicleModel.owner),
            selectinload(VehicleModel.organization),
        ])
        if result is None:
            raise AppExceptionResponse.not_found(message="ТС не найдено")
        return result

    async def create(self,
                     dto: VehicleCDTO,
                     repo: VehicleRepository = Depends(VehicleRepository),
                     vehicleColorRepos: VehicleColorRepository = Depends(VehicleColorRepository),
                     vehicleCategoryRepos: VehicleCategoryRepository = Depends(VehicleCategoryRepository),
                     regionRepo: RegionRepository = Depends(RegionRepository),
                     userRepo: UserRepository = Depends(UserRepository),
                     organizationRepo: OrganizationRepository = Depends(OrganizationRepository),

                     ):
        await self.check_form(dto, repo, vehicleColorRepos, vehicleCategoryRepos,
                              regionRepo, userRepo, organizationRepo, )
        result = await repo.create(VehicleModel(**dto.dict()))
        return result

    async def update(self,
                     dto: VehicleCDTO,
                     id: int = Path(gt=0),
                     repo: VehicleRepository = Depends(VehicleRepository),
                     vehicleColorRepos: VehicleColorRepository = Depends(VehicleColorRepository),
                     vehicleCategoryRepos: VehicleCategoryRepository = Depends(VehicleCategoryRepository),
                     regionRepo: RegionRepository = Depends(RegionRepository),
                     userRepo: UserRepository = Depends(UserRepository),
                     organizationRepo: OrganizationRepository = Depends(OrganizationRepository),
                     ):
        vehicle = await repo.get(id)
        if vehicle is None:
            raise AppExceptionResponse.not_found(message="ТС не найдено")
        await self.check_form(dto, repo, vehicleColorRepos, vehicleCategoryRepos,
                              regionRepo, userRepo, organizationRepo, id)
        result = await repo.update(obj=vehicle, dto=dto)
        return result

    async def delete(self, id: int = Path(gt=0), repo: VehicleRepository = Depends(VehicleRepository)):
        await repo.delete(id=id)

    @staticmethod
    async def check_form(
            dto: VehicleCDTO,
            repo: VehicleRepository,
            vehicleColorRepos: VehicleColorRepository,
            vehicleCategoryRepos: VehicleCategoryRepository,
            regionRepo: RegionRepository,
            userRepo: UserRepository,
            organizationRepo: OrganizationRepository,
            id: Optional[int] = None):
        existed_document_number = await repo.get_filtered({"document_number": dto.document_number})

        if existed_document_number is not None:
            if existed_document_number.id != id:
                raise AppExceptionResponse.bad_request(message="Такой номер свидетельства уже существует")

        existed_registration_number = await repo.get_filtered({"registration_number": dto.registration_number})

        if existed_registration_number is not None:
            if existed_registration_number.id != id:
                raise AppExceptionResponse.bad_request(message="Такой регистрационный номер уже существует")

        existed_vin = await repo.get_filtered({"vin": dto.vin})
        if existed_vin is not None:
            if existed_vin.id != id:
                raise AppExceptionResponse.bad_request(message="Такой ВИН номер уже существует")

        vehicle_color = await vehicleColorRepos.get(id=dto.color_id)
        if vehicle_color is None:
            raise AppExceptionResponse.bad_request(message="Такого цвета транспорта не существует")

        vehicle_category = await vehicleCategoryRepos.get(id=dto.category_id)
        if vehicle_category is None:
            raise AppExceptionResponse.bad_request(message="Такой категории ТС не существует")

        region = await regionRepo.get(id=dto.region_id)
        if region is None:
            raise AppExceptionResponse.bad_request(message="Такого региона не существует")

        if dto.owner_id is not None:
            owner = await userRepo.get(id=dto.owner_id)
            if owner is None:
                raise AppExceptionResponse.bad_request(message="Такого пользователя не существует")

        if dto.organization_id is not None:
            organization = await organizationRepo.get(id=dto.organization_id)
            if organization is None:
                raise AppExceptionResponse.bad_request(message="Такой организации не существует")
