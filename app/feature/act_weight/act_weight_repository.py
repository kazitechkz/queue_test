from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.act_weight_model import ActWeightModel


class ActWeightRepository(BaseRepository[ActWeightModel]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(ActWeightModel, db)