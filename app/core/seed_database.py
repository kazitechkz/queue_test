from datetime import date, time, datetime
import json
from pathlib import Path

from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from app.core.app_settings import AppSettings
from app.shared.database_constants import TableConstantsNames, AppTableNames


async def seed_database(db: Session) -> None:
    await add_roles(session=db)
    await add_user_types(session=db)
    await add_organization_types(session=db)
    await add_order_status(session=db)
    await add_sap_data(session=db)
    await add_operations(session=db)
    await add_vehicle_colors(session=db)
    await add_vehicle_categories(session=db)
    await add_regions(session=db)
    await add_users(session=db)
    await add_organizations(session=db)
    await add_vehicles(session=db)
    await add_workshop_schedules(session=db)


async def add_roles(session: Session) -> None:
    from app.domain.models.role_model import RoleModel
    await AppSeeder().load_seeders(session=session,BaseModel=RoleModel,table_name=AppTableNames.RoleTableName)



async def add_user_types(session: Session) -> None:
    from app.domain.models.user_type_model import UserTypeModel
    await AppSeeder().load_seeders(session=session,BaseModel=UserTypeModel,table_name=AppTableNames.UserTypeTableName)




async def add_organization_types(session: Session) -> None:
    from app.domain.models.organization_type_model import OrganizationTypeModel
    await AppSeeder().load_seeders(session=session,BaseModel=OrganizationTypeModel,table_name=AppTableNames.OrganizationTypeTableName)



async def add_order_status(session: Session) -> None:
    from app.domain.models.order_status_model import OrderStatusModel
    await AppSeeder().load_seeders(session=session,BaseModel=OrderStatusModel,table_name=AppTableNames.OrderStatusTableName)
    data = AppSeeder.get_data_from_file(f"{AppTableNames.OrderStatusTableName}_updated")
    for item in data:
        finded_items = await session.execute(
            select(OrderStatusModel).filter(OrderStatusModel.value == item["value"])
        )
        finded_item = finded_items.scalars().first()
        if finded_item is not None:
            finded_item.next_id = item["next_id"]
            finded_item.prev_id = item["prev_id"]
            await session.commit()


async def add_sap_data(session: Session) -> None:
    from app.domain.models.factory_model import FactoryModel
    from app.domain.models.material_model import MaterialModel
    from app.domain.models.workshop_model import WorkshopModel
    # Factory
    await AppSeeder().load_seeders(session=session, BaseModel=FactoryModel,
                                   table_name=AppTableNames.FactoryTableName)
    # Workshop
    await AppSeeder().load_seeders(session=session, BaseModel=WorkshopModel,
                                   table_name=AppTableNames.WorkshopTableName)
    # Material
    await AppSeeder().load_seeders(session=session, BaseModel=MaterialModel,
                                   table_name=AppTableNames.MaterialTableName)


async def add_operations(session: Session) -> None:
    from app.domain.models.operation_model import OperationModel
    await AppSeeder().load_seeders(session=session, BaseModel=OperationModel,
                                   table_name=AppTableNames.OperationTableName)
    data = AppSeeder.get_data_from_file(f"{AppTableNames.OperationTableName}_updated")
    for item in data:
        finded_items = await session.execute(
            select(OperationModel).filter(OperationModel.value == item["value"])
        )
        finded_item = finded_items.scalars().first()
        if finded_item is not None:
            finded_item.next_id = item["next_id"]
            finded_item.prev_id = item["prev_id"]
            await session.commit()

async def add_vehicle_colors(session: Session) -> None:
    from app.domain.models.vehicle_color_model import VehicleColorModel
    await AppSeeder().load_seeders(session=session, BaseModel=VehicleColorModel,
                                   table_name=AppTableNames.VehicleColorTableName)


async def add_vehicle_categories(session: Session) -> None:
    from app.domain.models.vehicle_category_model import VehicleCategoryModel
    await AppSeeder().load_seeders(session=session, BaseModel=VehicleCategoryModel,
                                   table_name=AppTableNames.VehicleCategoryTableName)


async def add_regions(session: Session) -> None:
    from app.domain.models.region_model import RegionModel
    await AppSeeder().load_seeders(session=session, BaseModel=RegionModel,
                                   table_name=AppTableNames.RegionTableName)


async def add_users(session: Session) -> None:
    from app.core.auth_core import get_password_hash
    from app.domain.models.user_model import UserModel
    data = [
        {**item, "password_hash": get_password_hash(item["password_hash"])}
        for item in AppSeeder.get_data_from_file(f"{AppTableNames.UserTableName}")
    ]
    await AppSeeder().load_seeders(session=session, BaseModel=UserModel,
                                   table_name=AppTableNames.UserTableName,ready_data=data)

async def add_organizations(session: Session) -> None:
    from app.domain.models.organization_model import OrganizationModel
    await AppSeeder().load_seeders(session=session, BaseModel=OrganizationModel,
                                   table_name=AppTableNames.OrganizationTableName)


async def add_vehicles(session: Session) -> None:
    from app.domain.models.vehicle_model import VehicleModel
    data = [
        {
            **item,
            "start_at": datetime.fromisoformat(item["start_at"])
        }
        for item in AppSeeder.get_data_from_file(f"{AppTableNames.VehicleTableName}")
    ]
    await AppSeeder().load_seeders(session=session, BaseModel=VehicleModel,
                                   table_name=AppTableNames.VehicleTableName,ready_data=data)


async def add_workshop_schedules(session: Session) -> None:
    from app.domain.models.workshop_schedule_model import WorkshopScheduleModel
    data = [
        {
            **item,
            "date_start": datetime.fromisoformat(item["date_start"]).date(),
            "date_end": datetime.fromisoformat(item["date_end"]).date(),
            "start_at": datetime.fromisoformat(f"2024-01-01T{item['start_at']}").time(),
            "end_at": datetime.fromisoformat(f"2024-01-01T{item['end_at']}").time(),
    }
        for item in AppSeeder.get_data_from_file(f"{AppTableNames.WorkshopScheduleTableName}")
    ]
    await AppSeeder().load_seeders(session=session, BaseModel=WorkshopScheduleModel,
                                   table_name=AppTableNames.WorkshopScheduleTableName,ready_data=data)


class AppSeeder:

    @staticmethod
    def get_seeders_path(filename: str) -> str:
        base_path = Path("app/seeders")
        environment = AppSettings().APP_STATUS.lower()
        env_path = base_path / environment
        if not env_path.exists():
            raise FileNotFoundError(f"Папка с сидерами для среды {environment} не существует по пути: {env_path}")
        file_path = env_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Файл сидера {filename} не существует по пути: {file_path}")
        return str(file_path)

    @staticmethod
    def get_data_from_file(filename: str):
        try:
            seeder_path = AppSeeder.get_seeders_path(f"{filename}.json")
        except FileNotFoundError as e:
            raise ValueError(f"Ошибка загрузки файла: {e}")
        try:
            with open(seeder_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка разбора JSON в файле {seeder_path}: {e}")


    async def load_seeders(self,BaseModel,session,table_name:str,ready_data:any=None):
        count_query = select(func.count()).select_from(BaseModel)
        total_items = await session.scalar(count_query)
        if total_items == 0:
            if ready_data is None:
                data = self.get_data_from_file(filename=table_name)
            else:
                data = ready_data
            loaded_data = [BaseModel(**item) for item in data]
            session.add_all(loaded_data)
            await session.commit()
            if AppSettings().APP_DATABASE == "postgresql":
                await session.execute(
                    text(f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), MAX(id)) FROM {table_name}")
                )
