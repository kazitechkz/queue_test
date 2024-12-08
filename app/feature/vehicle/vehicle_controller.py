from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import (
    check_admin,
    check_client,
    check_legal_client,
    get_current_user,
)
from app.core.pagination_dto import PaginationVehicleWithRelationsDTO
from app.domain.models.vehicle_model import VehicleModel
from app.feature.organization.organization_repository import OrganizationRepository
from app.feature.region.region_repository import RegionRepository
from app.feature.user.user_repository import UserRepository
from app.feature.vehicle.dtos.vehicle_dto import (
    VehicleCDTO,
    VehicleRDTO,
    VehicleWithRelationsDTO,
)
from app.feature.vehicle.filter.vehicle_filter import OwnVehicleFilter, VehicleFilter
from app.feature.vehicle.vehicle_repository import VehicleRepository
from app.feature.vehicle_category.vehicle_category_repository import (
    VehicleCategoryRepository,
)
from app.feature.vehicle_color.vehicle_color_repository import VehicleColorRepository
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class VehicleController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            "/",
            response_model=PaginationVehicleWithRelationsDTO,
            summary="Список транспортных средств",
            description="Получение списка транспортных средств",
        )(self.all)
        self.router.post(
            "/create",
            response_model=VehicleRDTO,
            summary="Создать транспортное средство",
            description="Создание транспортного средства",
        )(self.create)
        self.router.post(
            "/add-vehicle",
            response_model=VehicleRDTO,
            summary="Добавить транспортное средство",
            description="Добавление транспортных средств",
        )(self.add_vehicle)
        self.router.get(
            "/get/{id}",
            response_model=VehicleWithRelationsDTO,
            summary="Получение транспортного средства по ID",
            description="Получение транспортного средства по ID",
        )(self.get)
        self.router.get(
            "/get-own-cars",
            summary="Получение списка транспортных средств пользователя",
            description="Получение списка транспортных средств пользователя",
        )(self.get_own_cars)
        self.router.get(
            "/get-organization-cars/{organization_id}",
            summary="Получение списка транспортных средств организации",
            description="Получение списка транспортных средств организации",
        )(self.get_organization_cars)
        self.router.put(
            "/update/{id}",
            response_model=VehicleRDTO,
            summary="Обновление транспортного средства по ID",
            description="Обновление транспортного средства по ID",
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            summary="Удаление транспортного средства по ID",
            description="Удаление транспортного средства по ID",
        )(self.delete)

    async def all(
        self,
        params: VehicleFilter = Depends(),
        repo: VehicleRepository = Depends(VehicleRepository),
        current_user=Depends(check_admin),
    ):
        result = await repo.paginate_with_filter(
            dto=VehicleWithRelationsDTO,
            page=params.page,
            per_page=params.per_page,
            filters=params.apply(),
            options=[
                selectinload(VehicleModel.category),
                selectinload(VehicleModel.color),
                selectinload(VehicleModel.region),
                selectinload(VehicleModel.owner),
                selectinload(VehicleModel.organization),
            ],
        )
        return result

    async def get(
        self,
        id: int = Path(gt=0),
        repo: VehicleRepository = Depends(VehicleRepository),
        current_user=Depends(get_current_user),
    ):
        result = await repo.get(
            id=id,
            options=[
                selectinload(VehicleModel.category),
                selectinload(VehicleModel.color),
                selectinload(VehicleModel.region),
                selectinload(VehicleModel.owner),
                selectinload(VehicleModel.organization),
            ],
        )
        if result is None:
            raise AppExceptionResponse.not_found(message="ТС не найдено")
        return result

    async def get_own_cars(
        self,
        params: OwnVehicleFilter = Depends(),
        repo: VehicleRepository = Depends(VehicleRepository),
        userRDTO: UserRDTOWithRelations = Depends(check_client),
    ):
        result = await repo.get_all_with_filter(filters=params.apply(userRDTO))

        if result is None:
            raise AppExceptionResponse.not_found(message="ТС не найдено")
        return result

    async def get_organization_cars(
        self,
        organization_id: int = Path(gt=0),
        userRDTO: UserRDTOWithRelations = Depends(check_legal_client),
        repo: VehicleRepository = Depends(VehicleRepository),
    ):
        organization_ids = [organization.id for organization in userRDTO.organizations]
        if organization_id not in organization_ids:
            raise AppExceptionResponse.not_found(message="Организация не найдена")
        return await repo.get_all_with_filter(
            filters=[repo.model.organization_id.in_(organization_ids)]
        )

    async def create(
        self,
        dto: VehicleCDTO,
        repo: VehicleRepository = Depends(VehicleRepository),
        vehicleColorRepos: VehicleColorRepository = Depends(VehicleColorRepository),
        vehicleCategoryRepos: VehicleCategoryRepository = Depends(
            VehicleCategoryRepository
        ),
        regionRepo: RegionRepository = Depends(RegionRepository),
        userRepo: UserRepository = Depends(UserRepository),
        organizationRepo: OrganizationRepository = Depends(OrganizationRepository),
        current_user=Depends(check_admin),
    ):
        await self.check_form(
            dto,
            repo,
            vehicleColorRepos,
            vehicleCategoryRepos,
            regionRepo,
            userRepo,
            organizationRepo,
        )
        result = await repo.create(VehicleModel(**dto.dict()))
        return result

    async def add_vehicle(
        self,
        dto: VehicleCDTO,
        userRDTO: UserRDTOWithRelations = Depends(check_client),
        repo: VehicleRepository = Depends(VehicleRepository),
        vehicleColorRepos: VehicleColorRepository = Depends(VehicleColorRepository),
        vehicleCategoryRepos: VehicleCategoryRepository = Depends(
            VehicleCategoryRepository
        ),
        regionRepo: RegionRepository = Depends(RegionRepository),
        userRepo: UserRepository = Depends(UserRepository),
        organizationRepo: OrganizationRepository = Depends(OrganizationRepository),
    ):
        await self.check_form(
            dto,
            repo,
            vehicleColorRepos,
            vehicleCategoryRepos,
            regionRepo,
            userRepo,
            organizationRepo,
            userRDTO=userRDTO,
        )
        result = await repo.create(VehicleModel(**dto.dict()))
        return result

    async def update(
        self,
        dto: VehicleCDTO,
        id: int = Path(gt=0),
        repo: VehicleRepository = Depends(VehicleRepository),
        vehicleColorRepos: VehicleColorRepository = Depends(VehicleColorRepository),
        vehicleCategoryRepos: VehicleCategoryRepository = Depends(
            VehicleCategoryRepository
        ),
        regionRepo: RegionRepository = Depends(RegionRepository),
        userRepo: UserRepository = Depends(UserRepository),
        organizationRepo: OrganizationRepository = Depends(OrganizationRepository),
        current_user=Depends(check_admin),
    ):
        vehicle = await repo.get(id)
        if vehicle is None:
            raise AppExceptionResponse.not_found(message="ТС не найдено")
        await self.check_form(
            dto,
            repo,
            vehicleColorRepos,
            vehicleCategoryRepos,
            regionRepo,
            userRepo,
            organizationRepo,
            id,
        )
        result = await repo.update(obj=vehicle, dto=dto)
        return result

    async def delete(
        self,
        id: int = Path(gt=0),
        repo: VehicleRepository = Depends(VehicleRepository),
        current_user=Depends(check_admin),
    ) -> None:
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
        id: int | None = None,
        userRDTO: UserRDTOWithRelations | None = None,
    ) -> None:
        existed_document_number = await repo.get_filtered(
            {"document_number": dto.document_number}
        )

        if existed_document_number is not None:
            if existed_document_number.id != id:
                raise AppExceptionResponse.bad_request(
                    message="Такой номер свидетельства уже существует"
                )

        existed_registration_number = await repo.get_filtered(
            {"registration_number": dto.registration_number}
        )

        if existed_registration_number is not None:
            if existed_registration_number.id != id:
                raise AppExceptionResponse.bad_request(
                    message="Такой регистрационный номер уже существует"
                )

        existed_vin = await repo.get_filtered({"vin": dto.vin})
        if existed_vin is not None:
            if existed_vin.id != id:
                raise AppExceptionResponse.bad_request(
                    message="Такой ВИН номер уже существует"
                )

        vehicle_color = await vehicleColorRepos.get(id=dto.color_id)
        if vehicle_color is None:
            raise AppExceptionResponse.bad_request(
                message="Такого цвета транспорта не существует"
            )

        vehicle_category = await vehicleCategoryRepos.get(id=dto.category_id)
        if vehicle_category is None:
            raise AppExceptionResponse.bad_request(
                message="Такой категории ТС не существует"
            )

        region = await regionRepo.get(id=dto.region_id)
        if region is None:
            raise AppExceptionResponse.bad_request(message="Такого региона не существует")

        if dto.owner_id is not None:
            if userRDTO is not None:
                if (
                    userRDTO.user_type.value
                    == TableConstantsNames.UserIndividualTypeValue
                ):
                    if dto.owner_id != userRDTO.id:
                        raise AppExceptionResponse.bad_request(
                            message="Такого пользователя не существует"
                        )
                else:
                    raise AppExceptionResponse.bad_request(
                        message="Данные владельца только для физических лиц"
                    )
            else:
                owner = await userRepo.get(id=dto.owner_id)
                if owner is None:
                    raise AppExceptionResponse.bad_request(
                        message="Такого пользователя не существует"
                    )

        if dto.organization_id is not None:
            if userRDTO is not None:
                if userRDTO.user_type.value == TableConstantsNames.UserLegalTypeValue:
                    organization_ids = [
                        organization.id for organization in userRDTO.organizations
                    ]
                    if dto.organization_id not in organization_ids:
                        raise AppExceptionResponse.bad_request(
                            message="У вас нет такой организации"
                        )
                else:
                    raise AppExceptionResponse.bad_request(
                        message="Данные организации только для юридических лиц"
                    )
            else:
                organization = await organizationRepo.get(id=dto.organization_id)
                if organization is None:
                    raise AppExceptionResponse.bad_request(
                        message="Такой организации не существует"
                    )
