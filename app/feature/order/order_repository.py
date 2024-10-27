from datetime import datetime
from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session, selectinload

from app.core.app_exception_response import AppExceptionResponse
from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.order_model import OrderModel
from app.feature.factory.factory_repository import FactoryRepository
from app.feature.material.material_repository import MaterialRepository
from app.feature.order.dtos.order_dto import OrderCDTO
from app.feature.organization.organization_repository import OrganizationRepository
from app.feature.sap_request.sap_request_repository import SapRequestRepository
from app.feature.sap_request.sap_request_service import SapRequestService
from app.feature.workshop.workshop_repository import WorkshopRepository
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class OrderRepository(BaseRepository[OrderModel]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(OrderModel, db)

    async def create_order(
            self,
            dto,
            userDTO: UserRDTOWithRelations,
            materialRepo: MaterialRepository,
            workshopRepo: WorkshopRepository,
            factoryRepo: FactoryRepository,
            sapRequestService: SapRequestService,
            sapRequestRepo: SapRequestRepository,
            organizationRepo: Optional[OrganizationRepository] = None,
            is_individual: bool = True
    ):
        # Retrieve material information and validate workshop and factory
        material_dict = await materialRepo.count_price(sap_id=dto.material_sap_id, quan=dto.quan_t)
        material = material_dict["material"]
        workshop = await workshopRepo.get(id=material.workshop_id)
        if workshop is None:
            raise AppExceptionResponse.bad_request(message="Цех не найден")
        factory = await factoryRepo.get(id=workshop.factory_id)
        if factory is None:
            raise AppExceptionResponse.bad_request(message="Завод не найден")

        # Set common order data
        order_data = {
            "status_id": 1,
            "factory_id": factory.id,
            "factory_sap_id": factory.sap_id,
            "workshop_id": workshop.id,
            "workshop_sap_id": workshop.sap_id,
            "material_id": material.id,
            "material_sap_id": material.sap_id,
            "quan_t": dto.quan_t,
            "price_without_taxes": material_dict["price_without_taxes"],
            "price_with_taxes": material_dict["price_with_taxes"],
            "end_at": datetime.now().replace(year=datetime.now().year + 1)
        }

        # Additional fields for individual or legal order
        if is_individual:
            order_data.update({
                "owner_id": userDTO.id,
                "iin": userDTO.iin,
                "name": userDTO.name
            })
        else:
            # Validate organization for legal order
            organization = await organizationRepo.get_first_with_filters(filters=[
                {"id": dto.organization_id}, {"owner_id": userDTO.id}
            ])
            if organization is None:
                raise AppExceptionResponse.bad_request(message="Организация не найдена")
            order_data.update({
                "organization_id": dto.organization_id,
                "bin": organization.bin,
                "dogovor": dto.dogovor
            })

        order = await self.create(obj=OrderModel(**order_data))
        sap_request = await sapRequestRepo.request_to_sap(order=order, sapService=sapRequestService)
        if sap_request is not None and not sap_request.is_failed:
            order.zakaz = sap_request.zakaz
            order.sap_id = sap_request.id
            order.status_id = 3
        else:
            order.status_id = 2

        order = await self.update(obj=order, dto=OrderCDTO.from_orm(order))
        return await self.get(id=order.id, options=[selectinload(OrderModel.material),
                selectinload(OrderModel.organization),
                selectinload(OrderModel.factory),
                selectinload(OrderModel.workshop),
                selectinload(OrderModel.kaspi),
                selectinload(OrderModel.sap_request),])

