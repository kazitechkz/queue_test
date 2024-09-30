from app.feature.auth.auth_controller import AuthController
from app.feature.factory.factory_controller import FactoryController
from app.feature.kaspi_payment.kaspi_payment_controller import KaspiPaymentController
from app.feature.material.material_controller import MaterialController
from app.feature.operation.operation_controller import OperationController
from app.feature.order.order_controller import OrderController
from app.feature.organization.organization_controller import OrganizationController
from app.feature.organization_employee.organization_employee_controller import OrganizationEmployeeController
from app.feature.organization_type.organization_type_controller import OrganizationTypeController
from app.feature.region.region_controller import RegionController
from app.feature.role.role_controller import RoleController
from app.feature.sap_request.sap_request_controller import SapRequestController
from app.feature.schedule.schedule_controller import ScheduleController
from app.feature.schedule_history.schedule_history_controller import ScheduleHistoryController
from app.feature.test.test_controller import TestController
from app.feature.user.user_controller import UserController
from app.feature.user_type.user_type_controller import UserTypeController
from app.feature.vehicle.vehicle_controller import VehicleController
from app.feature.vehicle_category.vehicle_category_controller import VehicleCategoryController
from app.feature.vehicle_color.vehicle_color_controller import VehicleColorController
from app.feature.workshop.workshop_controller import WorkshopController
from app.feature.workshop_schedule.workshop_schedule_controller import WorkshopScheduleController


def include_routers(app):
    app.include_router(RoleController().router, prefix="/role", tags=["role"])
    app.include_router(UserTypeController().router, prefix="/user-type", tags=["user-type"])
    app.include_router(UserController().router, prefix="/user", tags=["user"])
    app.include_router(OrganizationTypeController().router, prefix="/organization-type", tags=["organization-type"])
    app.include_router(OrganizationController().router, prefix="/organization", tags=["organization"])
    app.include_router(OrganizationEmployeeController().router, prefix="/organization-employee",
                       tags=["organization-employee"])
    app.include_router(VehicleColorController().router, prefix="/vehicle-color", tags=["vehicle-color"])
    app.include_router(VehicleCategoryController().router, prefix="/vehicle-category", tags=["vehicle-category"])
    app.include_router(RegionController().router, prefix="/region", tags=["region"])
    app.include_router(VehicleController().router, prefix="/vehicle", tags=["vehicle"])
    app.include_router(FactoryController().router, prefix="/factory", tags=["factory"])
    app.include_router(WorkshopController().router, prefix="/workshop", tags=["workshop"])
    app.include_router(MaterialController().router, prefix="/material", tags=["material"])
    app.include_router(AuthController().router, prefix="/auth", tags=["auth"])
    app.include_router(OrderController().router, prefix="/order", tags=["order"])
    app.include_router(SapRequestController().router, prefix="/sap-request", tags=["sap-request"])
    app.include_router(KaspiPaymentController().router, prefix="/kaspi", tags=["kaspi"])
    app.include_router(OperationController().router, prefix="/operation", tags=["operation"])
    app.include_router(WorkshopScheduleController().router, prefix="/workshop-schedule", tags=["workshop-schedule"])
    app.include_router(ScheduleController().router, prefix="/schedule", tags=["schedule"])
    app.include_router(ScheduleHistoryController().router, prefix="/schedule-history", tags=["schedule-history"])
    app.include_router(TestController().router, prefix="/test", tags=["test"])
