from datetime import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import mapped_column

ID = Annotated[int, mapped_column(primary_key=True)]
CreatedAt = Annotated[datetime, mapped_column(server_default=text("CURRENT_TIMESTAMP"))]
UpdatedAt = Annotated[datetime, mapped_column(server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.now())]


class AppTableNames():
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


class TableConstantsNames:
    #Roles
    RoleAdminValue = "admin"
    RoleSecurityValue = "security"
    RoleSecurityLoaderValue = "security_loader"
    RoleLoaderValue = "loader"
    RoleWeigherValue = "weigher"
    RoleClientValue = "client"

    #User Types
    UserLegalTypeValue = "legal_entity"
    UserIndividualTypeValue = "individual"

    #Organization Type
    OrganizationLLCTypeValue = "llc"
    OrganizationIPTypeValue = "ip"

    #OrderStatus
    OrderStatusWaitSap = "waiting_for_sup"
    OrderStatusRejectSap = "reject_from_sup"
    OrderStatusWaitPayment = "waiting_for_payment"
    OrderStatusRejectPayment = "reject_from_payment"
    OrderStatusPaid = "paid"
    OrderStatusExecuted = "executed"
    OrderStatusFinished = "finished"


