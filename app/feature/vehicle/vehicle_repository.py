from typing import List

from fastapi import Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.vehicle_model import VehicleModel
from app.feature.vehicle.dtos.vehicle_dto import VehicleRDTO
from app.feature.vehicle.filter.vehicle_filter import OwnVehicleFilter
from app.shared.relation_dtos.user_organization import UserRDTOWithRelations


class VehicleRepository(BaseRepository[VehicleModel]):

    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(VehicleModel, db)
