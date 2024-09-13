from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.app_exception_response import AppExceptionResponse
from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.order_model import OrderModel
from app.feature.factory.factory_repository import FactoryRepository
from app.feature.material.material_repository import MaterialRepository
from app.feature.order.dtos.order_dto import CreateIndividualOrderDTO
from app.feature.user.dtos.user_dto import UserRDTOWithRelations
from app.feature.workshop.workshop_repository import WorkshopRepository


class OrderRepository(BaseRepository[OrderModel]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(OrderModel, db)

    async def create_individual_order(
            self,
            dto:CreateIndividualOrderDTO,
            userDTO:UserRDTOWithRelations,
            materialRepo:MaterialRepository,
            workshopRepo:WorkshopRepository,
            factoryRepo:FactoryRepository
    ):
        material_dict = materialRepo.count_price(sap_id=dto.material_sap_id,quan=dto.quan)
        material = material_dict["material"]
        workshop = await workshopRepo.get(id=material.workshop_id)
        if workshop is None:
            raise AppExceptionResponse.bad_request(message="Цех не найден")
        factory = await factoryRepo.get(id=workshop.factory_id)
        if factory is None:
            raise AppExceptionResponse.bad_request(message="Завод не найден")
        order_data = OrderModel(
            status_id = 1,
            factory_id = factory.id,
            factory_sap_id = factory.sap_id,
            workshop_id=workshop.id,
            workshop_sap_id=workshop.sap_id,
            material_id=material.id,
            material_sap_id = material.sap_id,
            quan = dto.quan,
            price_without_taxes = material_dict["price_without_taxes"],
            price_with_taxes = material_dict["price_with_taxes"],
            owner_id = userDTO.id,
            iin = userDTO.iin,
            name = userDTO.name,
        )
        order = await self.create(obj=order_data)
