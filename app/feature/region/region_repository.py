from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.region_model import RegionModel


class RegionRepository(BaseRepository[RegionModel]):

    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(RegionModel, db)

