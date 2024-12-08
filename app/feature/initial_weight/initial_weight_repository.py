from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.initial_weight_model import InitialWeightModel


class InitialWeightRepository(BaseRepository[InitialWeightModel]):
    def __init__(self, db: Session = Depends(get_db)) -> None:
        super().__init__(InitialWeightModel, db)
