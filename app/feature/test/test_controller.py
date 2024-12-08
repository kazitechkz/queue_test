from fastapi import APIRouter, Depends

from app.feature.user.user_repository import UserRepository


class TestController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get("/test")(self.test)

    async def test(self, userRepo: UserRepository = Depends()):
        vehicle_tara_kg = 9500
        trailer_tara_kg = 6000
        (vehicle_tara_kg or 0) + (trailer_tara_kg or 0)
        return await userRepo.get_admin()
