from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import selectinload

from app.feature.baseline_weight.baseline_weight_repository import BaselineWeightRepository
from app.feature.operation.operation_repository import OperationRepository
from app.feature.schedule_history.schedule_history_repository import ScheduleHistoryRepository
from app.feature.user.user_repository import UserRepository


class TestController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/test")(self.test)

    async def test(self, userRepo: UserRepository = Depends()):
        vehicle_tara_kg = 9500
        trailer_tara_kg = 6000
        total_weight = (vehicle_tara_kg or 0) + (trailer_tara_kg or 0)
        print(total_weight)
        return await userRepo.get_admin()
