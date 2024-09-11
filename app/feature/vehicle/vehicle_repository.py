from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.vehicle_model import VehicleModel


class VehicleRepository(BaseRepository[VehicleModel]):

    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(VehicleModel, db)

