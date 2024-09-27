from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import check_individual_client, check_legal_client, check_client
from app.domain.models.order_model import OrderModel
from app.feature.factory.factory_repository import FactoryRepository
from app.feature.material.material_repository import MaterialRepository
from app.feature.order.dtos.order_dto import CreateIndividualOrderDTO, CreateLegalOrderDTO, OrderRDTOWithRelations
from app.feature.order.filter.order_filter import OrderFilter
from app.feature.order.order_repository import OrderRepository
from app.feature.organization.organization_repository import OrganizationRepository
from app.feature.sap_request.sap_request_repository import SapRequestRepository
from app.feature.sap_request.sap_request_service import SapRequestService
from app.feature.workshop.workshop_repository import WorkshopRepository
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class OrderController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/get-all-order", )(self.get_all)
        self.router.get("/get-detail-order/{order_id}", )(self.get_detail_order)
        self.router.post("/create-individual-order", )(self.create_individual)
        self.router.post("/create-legal-order", )(self.create_legal)

    async def get_all(
            self,
            params: OrderFilter = Depends(),
            repo: OrderRepository = Depends(OrderRepository),
            userRDTO: UserRDTOWithRelations = Depends(check_client)
    ):
        result = await repo.paginate_with_filter(dto=OrderRDTOWithRelations, page=params.page, per_page=params.per_page,
                                                 filters=params.apply(userRDTO), options=[
                selectinload(OrderModel.material),
                selectinload(OrderModel.organization),
                selectinload(OrderModel.factory),
                selectinload(OrderModel.workshop),
                selectinload(OrderModel.kaspi),
            ])

        return result

    async def get_detail_order(self, order_id: int = Path(gt=0), repo: OrderRepository = Depends(OrderRepository)):
        result = await repo.get(id=order_id, options=[
            selectinload(OrderModel.factory),
            selectinload(OrderModel.workshop),
            selectinload(OrderModel.kaspi),
            selectinload(OrderModel.organization),
        ])
        if result is None:
            raise AppExceptionResponse.not_found(message="Заказ не найден")
        return result


    async def create_individual(self,
                                dto: CreateIndividualOrderDTO,
                                repo: OrderRepository = Depends(OrderRepository),
                                userRDTO: UserRDTOWithRelations = Depends(check_individual_client),
                                materialRepo: MaterialRepository = Depends(MaterialRepository),
                                workshopRepo: WorkshopRepository = Depends(WorkshopRepository),
                                factoryRepo: FactoryRepository = Depends(FactoryRepository),
                                sapRequestService: SapRequestService = Depends(SapRequestService),
                                sapRequestRepo: SapRequestRepository = Depends(SapRequestRepository),
                                ):
        result = await repo.create_order(
            dto=dto,
            userDTO=userRDTO,
            materialRepo=materialRepo,
            workshopRepo=workshopRepo,
            factoryRepo=factoryRepo,
            sapRequestService=sapRequestService,
            sapRequestRepo=sapRequestRepo,
            is_individual=True
        )
        return result

    async def create_legal(self,
                           dto: CreateLegalOrderDTO,
                           repo: OrderRepository = Depends(OrderRepository),
                           userRDTO: UserRDTOWithRelations = Depends(check_legal_client),
                           organizationRepo: OrganizationRepository = Depends(OrganizationRepository),
                           materialRepo: MaterialRepository = Depends(MaterialRepository),
                           workshopRepo: WorkshopRepository = Depends(WorkshopRepository),
                           factoryRepo: FactoryRepository = Depends(FactoryRepository),
                           sapRequestService: SapRequestService = Depends(SapRequestService),
                           sapRequestRepo: SapRequestRepository = Depends(SapRequestRepository),
                           ):
        result = await repo.create_order(
            dto=dto,
            userDTO=userRDTO,
            organizationRepo=organizationRepo,
            materialRepo=materialRepo,
            workshopRepo=workshopRepo,
            factoryRepo=factoryRepo,
            sapRequestService=sapRequestService,
            sapRequestRepo=sapRequestRepo,
            is_individual=False
        )
        return result
