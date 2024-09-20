import datetime

from fastapi import APIRouter


class TestController:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/test")(self.test)

    async def test(self):
        return datetime.datetime.now()
