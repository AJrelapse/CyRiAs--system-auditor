from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class IdentityType(str, Enum):
    USER = "user"
    SERVICE_ACCOUNT = "service_account"
    GROUP = "group"


class IdentityStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"


class Identity(BaseModel):

    identity_id: str

    name: str

    identity_type: IdentityType

    email: str | None = None

    department: str | None = None

    status: IdentityStatus = IdentityStatus.ACTIVE

    groups: list[str] = Field(
        default_factory=list
    )

    roles: list[str] = Field(
        default_factory=list
    )

    direct_permissions: list[str] = Field(
        default_factory=list
    )

    effective_permissions: list[str] = Field(
        default_factory=list
    )

    accessible_assets: list[str] = Field(
        default_factory=list
    )


class IdentitySyncResult(BaseModel):

    total_identities: int

    created: list[str]

    modified: list[str]

    deleted: list[str]

    unchanged: list[str]


class IdentityResponse(BaseModel):

    identity_id: str

    name: str

    identity_type: str

    email: str | None

    department: str | None

    status: str

    groups: str

    roles: str

    direct_permissions: str

    effective_permissions: str

    accessible_assets: str

    created_at: datetime

    updated_at: datetime


    model_config = {
        "from_attributes": True
    }


class IdentityDeltaEventResponse(BaseModel):

    event_id: str

    identity_id: str

    change_type: str

    changed_fields: str | None

    previous_state: str | None

    current_state: str | None

    created_at: datetime


    model_config = {
        "from_attributes": True
    }