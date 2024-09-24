import datetime

from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.core.app_exception_response import AppExceptionResponse
from app.core.base_repository import BaseRepository
from app.core.database import get_db
from app.domain.models.schedule_model import ScheduleModel
from app.domain.models.workshop_schedule_model import WorkshopScheduleModel


class WorkshopScheduleRepository(BaseRepository[WorkshopScheduleModel]):

    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(WorkshopScheduleModel, db)





