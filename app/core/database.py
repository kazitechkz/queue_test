from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.app_settings import app_settings
from app.core.seed_database import seed_database
engine_async = create_async_engine(
    app_settings.DB_URL_ASYNC,
    echo=False,
    pool_size=100,
    max_overflow=50,
    pool_timeout=300,
    pool_recycle=25000,
)

AsyncSessionLocal = sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


class Base(DeclarativeBase):
    pass


async def init_db():
    from app.domain.models.role_model import RoleModel
    from app.domain.models.user_type_model import UserTypeModel
    from app.domain.models.user_model import UserModel
    from app.domain.models.organization_type_model import OrganizationTypeModel
    from app.domain.models.organization_model import OrganizationModel
    from app.domain.models.organization_employee_model import OrganizationEmployeeModel
    from app.domain.models.vehicle_model import VehicleModel
    from app.domain.models.factory_model import FactoryModel
    from app.domain.models.workshop_model import WorkshopModel
    from app.domain.models.material_model import MaterialModel
    from app.domain.models.order_status_model import OrderStatusModel
    from app.domain.models.order_model import OrderModel
    from app.domain.models.sap_request_model import SapRequestModel
    from app.domain.models.kaspi_payment_model import KaspiPaymentModel
    from app.domain.models.operation_model import OperationModel
    from app.domain.models.workshop_schedule_model import WorkshopScheduleModel
    from app.domain.models.schedule_model import ScheduleModel
    from app.domain.models.schedule_history_model import ScheduleHistoryModel
    from app.domain.models.initial_weight_model import InitialWeightModel
    from app.domain.models.act_weight_model import ActWeightModel
    from app.domain.models.access_token_model import AccessTokenModel
    from app.domain.models.baseline_weights_model import BaselineWeightModel
    from app.domain.models.file_model import FileModel
    from app.domain.models.payment_document_model import PaymentDocumentModel

    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        await seed_database(session)
