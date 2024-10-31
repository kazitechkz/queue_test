from datetime import datetime
from typing import List

from fastapi import Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.baseline_weights_model import BaselineWeightModel


class BaselineWeightRepository(BaseRepository[BaselineWeightModel]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(BaselineWeightModel, db)

    async def get_vehicle_trailer_weights(
            self,
            ids: List[int]
    ):
        return await self.get_all_with_filter(
            filters=[and_(self.model.vehicle_id.in_(ids), self.model.end_at > datetime.now())],
        )
