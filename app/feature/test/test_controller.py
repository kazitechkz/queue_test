from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import selectinload

from app.feature.operation.operation_repository import OperationRepository


class TestController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/test")(self.test)

    async def test(self,operationRepos:OperationRepository = Depends()):
        return await operationRepos.get_all_with_filter(options=[selectinload(operationRepos.model.role),])
