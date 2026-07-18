from .models import (
    Identity,
    IdentityType,
)


def get_mock_identities() -> list[Identity]:

    return [

        # Finance employee

        Identity(

            identity_id="USR-001",

            name="Finance User",

            identity_type=(
                IdentityType.USER
            ),

            email=(
                "finance.user@example.local"
            ),

            department="Finance",

            groups=[
                "GRP-FINANCE"
            ],

            roles=[
                "FinanceUser"
            ],

            direct_permissions=[],

            effective_permissions=[
                "customer_data:read",
                "financial_reports:read",
                "database:admin",
            ],

            accessible_assets=[
                "END-001",
                "APP-001",
                "DB-001",
            ],
        ),


        # System administrator

        Identity(

            identity_id="USR-002",

            name="System Administrator",

            identity_type=(
                IdentityType.USER
            ),

            email=(
                "admin@example.local"
            ),

            department="IT",

            groups=[
                "GRP-ADMINS"
            ],

            roles=[
                "SystemAdministrator"
            ],

            direct_permissions=[
                "server:admin"
            ],

            effective_permissions=[
                "server:admin",
                "identity:admin",
                "database:admin",
            ],

            accessible_assets=[
                "SRV-001",
                "SRV-002",
                "DB-001",
            ],
        ),


        # Application service identity

        Identity(

            identity_id="SVC-001",

            name=(
                "Customer Application "
                "Service Account"
            ),

            identity_type=(
                IdentityType
                .SERVICE_ACCOUNT
            ),

            department="Application",

            groups=[],

            roles=[
                "DatabaseApplicationRole"
            ],

            direct_permissions=[],

            effective_permissions=[
                "database:connect",
                "database:read",
            ],

            accessible_assets=[
                "APP-001",
                "DB-001",
            ],
        ),


        # Finance group

        Identity(

            identity_id="GRP-FINANCE",

            name="Finance Employees",

            identity_type=(
                IdentityType.GROUP
            ),

            department="Finance",

            groups=[],

            roles=[
                "FinanceUser"
            ],

            direct_permissions=[
                "financial_reports:read"
            ],

            effective_permissions=[
                "financial_reports:read"
            ],

            accessible_assets=[
                "APP-001"
            ],
        ),


        # Administrator group

        Identity(

            identity_id="GRP-ADMINS",

            name="Enterprise Administrators",

            identity_type=(
                IdentityType.GROUP
            ),

            department="IT",

            groups=[],

            roles=[
                "SystemAdministrator"
            ],

            direct_permissions=[
                "server:admin",
                "identity:admin",
            ],

            effective_permissions=[
                "server:admin",
                "identity:admin",
                "database:admin",
            ],

            accessible_assets=[
                "SRV-001",
                "SRV-002",
                "DB-001",
            ],
        ),

    ]