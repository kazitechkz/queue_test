from fastapi import APIRouter, Depends

from app.core.auth_core import check_individual_client, check_legal_client, check_client
from app.feature.factory.factory_repository import FactoryRepository
from app.feature.material.material_repository import MaterialRepository
from app.feature.order.dtos.order_dto import CreateIndividualOrderDTO, CreateLegalOrderDTO, OrderRDTO
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
        self.router.post("/get-all-order", )(self.get_all)
        self.router.post("/create-individual-order", )(self.create_individual)
        self.router.post("/create-legal-order", )(self.create_legal)

    async def get_all(
            self,
            params: OrderFilter = Depends(),
            repo: OrderRepository = Depends(OrderRepository),
            userRDTO: UserRDTOWithRelations = Depends(check_client)
    ):
        # owner_ids = [org.owner_id for org in userRDTO.organizations]
        # return owner_ids
        # return params.apply(userRDTO)
        result = await repo.paginate_with_filter(dto=OrderRDTO, page=params.page, per_page=params.per_page,
                                                 filters=params.apply(userRDTO))
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
