from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_

from app.core.auth_core import get_current_user
from app.feature.baseline_weight.baseline_weight_repository import BaselineWeightRepository
from app.feature.baseline_weight.dtos.baseline_weight_dto import BaselineWeightRDTO
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class BaselineWeightController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get(
            "/get-vehicle-trailer-weights",
            response_model=List[BaselineWeightRDTO],
            summary="Получить все данные первичного веса нескольких транспортных средств",
            description="Получить все данные первичного веса нескольких транспортных средств по уникальным "
                        "идентификаторам транспортных средств "
        )(self.get_vehicle_trailer_weights)
        self.router.get(
            "/get/{vehicle-id}",
            response_model=List[BaselineWeightRDTO],
            summary="Получить данные первичного веса для транспортного средства",
            description="Получить данные первичного веса для транспортного средства по его уникальному ID"
        )(self.get)

    async def get_vehicle_trailer_weights(
            self,
            ids: List[int] = Query(description="Идентфикаторы транспортных средств"),
            repo: BaselineWeightRepository = Depends(BaselineWeightRepository),
            userRDTO: UserRDTOWithRelations = Depends(get_current_user),
    ):
        return await repo.get_all_with_filter(
            filters=[and_(repo.model.vehicle_id.in_(ids), repo.model.end_at > datetime.now())],
        )

    async def get(
            self,
            vehicle_id: int,
            repo: BaselineWeightRepository = Depends(BaselineWeightRepository),
            userRDTO: UserRDTOWithRelations = Depends(get_current_user)):
        return await repo.get_first_with_filters(
            filters=[and_(repo.model.vehicle_id == vehicle_id)],
        )
