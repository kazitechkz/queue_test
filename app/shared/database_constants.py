from datetime import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import mapped_column

ID = Annotated[int, mapped_column(primary_key=True)]
CreatedAt = Annotated[datetime, mapped_column(server_default=text("CURRENT_TIMESTAMP"))]
UpdatedAt = Annotated[datetime, mapped_column(server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.now())]


class AppTableNames:
    RoleTableName = "roles"
    UserTypeTableName = "user_types"
    UserTableName = "users"
    OrganizationTypeTableName = "organization_types"
    OrganizationTableName = "organizations"
    OrganizationEmployeeTableName = "organization_employees"
    VehicleColorTableName = "vehicle_colors"
    VehicleCategoryTableName = "vehicle_categories"
    RegionTableName = "regions"
    VehicleTableName = "vehicles"
    FactoryTableName = "factories"
    WorkshopTableName = "workshops"
    MaterialTableName = "materials"
    OrderStatusTableName = "order_status"
    OrderTableName = "orders"
    SAPRequestTableName = "sap_requests"
    KaspiPaymentsTableName = "kaspi_payments"
    OperationTableName = "operations"
    WorkshopScheduleTableName = "workshop_schedules"
    ScheduleTableName = "schedules"
    ScheduleHistoryTableName = "schedule_histories"
    InitialWeightTableName = "initial_weights"
    ActWeightTableName = "act_weights"
    EmployeeRequestTableName = "employee_requests"


class TableConstantsNames:
    # Roles
    RoleAdminValue = "admin"
    RoleAdminId = 1
    RoleSecurityValue = "security"
    RoleSecurityId = 2
    RoleSecurityLoaderValue = "security_loader"
    RoleSecurityLoaderId = 3
    RoleLoaderValue = "loader"
    RoleLoaderId = 4
    RoleWeigherValue = "weigher"
    RoleWeigherId = 5
    RoleClientValue = "client"
    RoleClientId = 6

    # User Types
    UserLegalTypeValue = "legal_entity"
    UserLegalTypeId = 2
    UserIndividualTypeValue = "individual"
    UserIndividualTypeId = 1

    # Organization Type
    OrganizationLLCTypeValue = "llc"
    OrganizationIPTypeValue = "ip"

    # OrderStatus
    OrderStatusWaitSap = "waiting_for_sup"
    OrderStatusRejectSap = "reject_from_sup"
    OrderStatusWaitPayment = "waiting_for_payment"
    OrderStatusRejectPayment = "reject_from_payment"
    OrderStatusExecuted = "executed"
    OrderStatusFinished = "finished"
    OrderStatusCanceled = "canceled"

    # Operations
    EntryOperationName = "entry_operation"
    EntryOperationId = 1
    InitialWeightOperationName = "initial_weight_operation"
    InitialWeightOperationId = 2
    LoadingEntryOperationName = "loading_entry_operation"
    LoadingEntryOperationId = 3
    LoadingOperationName = "loading_operation"
    LoadingOperationId = 4
    FinalWeightOperationName = "final_weight_operation"
    FinalWeightOperationId = 5
    ExitCheckOperationName = "exit_check_operation"
    ExitCheckOperationId = 6
    ReLoadingEntryExitOperationName = "reloading_entry_exit_operation"
    ReLoadingEntryExitOperationId = 7
    ReLoadingExitOperationName = "reloading_exit_operation"
    ReLoadingExitOperationId = 8
    ReLoadingEntryWeightOperationName = "reloading_entry_weight_operation"
    ReLoadingEntryWeightOperationId = 9
    ReLoadingWeightOperationName = "reloading_weight_operation"
    ReLoadingWeightOperationId = 10
    ExecutedOperationName = "executed_operation"
    ExecutedOperationId = 11

    RELOAD_OPERATIONS = [ReLoadingEntryExitOperationName, ReLoadingEntryWeightOperationName]
