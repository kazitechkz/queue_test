from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import selectinload

from app.feature.initial_weight.dtos.initial_weight_dto import InitialWeightRelationsDTO
from app.feature.initial_weight.filter.InitialWeightFilter import InitialWeightFilter
from app.feature.initial_weight.initial_weight_repository import InitialWeightRepository


class InitialWeightController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get("/all")(self.all)
        self.router.get("/get/{id}", response_model=InitialWeightRelationsDTO)(self.get)

    # Only for admin and employee
    async def all(
        self,
        params: InitialWeightFilter = Depends(InitialWeightFilter),
        repo: InitialWeightRepository = Depends(InitialWeightRepository),
    ):
        result = await repo.paginate_with_filter(
            dto=InitialWeightRelationsDTO,
            page=params.page,
            per_page=params.per_page,
            filters=params.apply(),
            options=[
                selectinload(repo.model.history),
                selectinload(repo.model.responsible),
                selectinload(repo.model.order),
                selectinload(repo.model.vehicle),
                selectinload(repo.model.trailer),
            ],
        )
        return result

    async def get(
        self,
        id: int = Path(gt=0, description="Идентификатор акта первичного взвешивания"),
        repo: InitialWeightRepository = Depends(InitialWeightRepository),
    ) -> InitialWeightRelationsDTO:
        result = await repo.get(
            id=id,
            options=[
                selectinload(repo.model.history),
                selectinload(repo.model.responsible),
                selectinload(repo.model.order),
                selectinload(repo.model.vehicle),
                selectinload(repo.model.trailer),
            ],
        )
        result_dto = InitialWeightRelationsDTO.from_orm(result)
        return result_dto
