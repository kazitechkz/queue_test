import datetime
from typing import List

from fastapi import APIRouter, Depends, Path
from sqlalchemy import and_
from sqlalchemy.orm import selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import check_individual_client, check_legal_client, get_current_user, check_client
from app.domain.models.order_model import OrderModel
from app.domain.models.schedule_history_model import ScheduleHistoryModel
from app.domain.models.schedule_model import ScheduleModel
from app.domain.models.workshop_model import WorkshopModel
from app.domain.models.workshop_schedule_model import WorkshopScheduleModel
from app.feature.factory.factory_repository import FactoryRepository
from app.feature.material.material_repository import MaterialRepository
from app.feature.order.dtos.order_dto import CreateIndividualOrderDTO, CreateLegalOrderDTO, OrderRDTOWithRelations
from app.feature.order.filter.order_filter import OrderFilter, DetailOrderFilter
from app.feature.order.order_repository import OrderRepository
from app.feature.organization.organization_repository import OrganizationRepository
from app.feature.sap_request.sap_request_repository import SapRequestRepository
from app.feature.sap_request.sap_request_service import SapRequestService
from app.feature.schedule.schedule_repository import ScheduleRepository
from app.feature.schedule_history.schedule_history_repository import ScheduleHistoryRepository
from app.feature.workshop.workshop_repository import WorkshopRepository
from app.shared.database_constants import TableConstantsNames
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class OrderController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/check-order-payment")(self.check_order_payment)
        self.router.get("/get-all-order")(self.get_all)
        self.router.get("/get-detail-order")(self.get_detail_order)
        self.router.get("/my-paid-orders",response_model=List[OrderRDTOWithRelations])(self.my_paid_orders)
        self.router.post("/create-individual-order")(self.create_individual)
        self.router.post("/create-legal-order")(self.create_legal)

    async def get_all(
            self,
            params: OrderFilter = Depends(),
            repo: OrderRepository = Depends(OrderRepository),
            userRDTO: UserRDTOWithRelations = Depends(get_current_user)
    ):
        result = await repo.paginate_with_filter(dto=OrderRDTOWithRelations, page=params.page, per_page=params.per_page,
                                                 filters=params.apply(userRDTO), options=[
                selectinload(OrderModel.material),
                selectinload(OrderModel.organization),
                selectinload(OrderModel.factory),
                selectinload(OrderModel.workshop),
                selectinload(OrderModel.kaspi),
                selectinload(OrderModel.sap_request),
            ])

        return result

    async def my_paid_orders(
            self,
            userDTO:UserRDTOWithRelations = Depends(check_client),
            repo: OrderRepository = Depends(OrderRepository),

    ):
        filters = [and_(repo.model.is_active == True, repo.model.is_paid == True)]
        if userDTO.user_type.value == TableConstantsNames.UserIndividualTypeValue:
            filters.append(and_(repo.model.owner_id == userDTO.id))
        elif userDTO.user_type.value == TableConstantsNames.UserLegalTypeValue:
            owner_ids = [org.id for org in userDTO.organizations]
            filters.append(and_(repo.model.organization_id.in_(owner_ids)))
        result = await repo.get_all_with_filter(
            filters=filters, options=[
                selectinload(repo.model.material),
                selectinload(repo.model.organization),
                selectinload(repo.model.factory),
                selectinload(repo.model.workshop),
                selectinload(repo.model.kaspi),
                selectinload(repo.model.sap_request),
            ])
        result_dto = [OrderRDTOWithRelations.from_orm(resultItem) for resultItem in result]
        return result_dto

    async def get_detail_order(
            self,
            filters: DetailOrderFilter = Depends(DetailOrderFilter),
            repo: OrderRepository = Depends(OrderRepository),
            userRDTO: UserRDTOWithRelations = Depends(get_current_user)
    ):
        result = await repo.get_with_filter(filters=filters.apply(userDTO=userRDTO), options=[
            selectinload(OrderModel.factory),
            selectinload(OrderModel.workshop),
            selectinload(OrderModel.kaspi),
            selectinload(OrderModel.organization),
            selectinload(OrderModel.sap_request),
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


    async def check_order_payment(self,repo: OrderRepository = Depends(OrderRepository)):
        filters = [and_(repo.model.is_active == True, repo.model.txn_id == None, repo.model.must_paid_at < datetime.datetime.now())]
        updated_values = {"status_id":7,"is_active":False,"is_finished":False,"is_paid":False, "is_failed":True}
        return await repo.update_with_filters(update_values=updated_values,filters=filters)

