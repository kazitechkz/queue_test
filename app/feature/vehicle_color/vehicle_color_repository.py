from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.vehicle_color_model import VehicleColorModel


class VehicleColorRepository(BaseRepository[VehicleColorModel]):
    def __init__(self, db: Session = Depends(get_db)) -> None:
        super().__init__(VehicleColorModel, db)
