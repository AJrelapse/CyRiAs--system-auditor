from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class CloudResourceType(str, Enum):
    VIRTUAL_MACHINE = "virtual_machine"
    DATABASE = "database"
    STORAGE = "storage"
    SECURITY_GROUP = "security_group"
    LOAD_BALANCER = "load_balancer"
    IAM_ROLE = "iam_role"


class CloudChangeType(str, Enum):
    CREATED = "CREATED"
    MODIFIED = "MODIFIED"
    DELETED = "DELETED"


class CloudResource(BaseModel):
    resource_id: str
    asset_id: Optional[str] = None

    name: str
    resource_type: CloudResourceType

    provider: str
    region: str

    status: str = "active"

    configuration: dict[str, Any] = Field(
        default_factory=dict
    )


class CloudSyncResult(BaseModel):
    total_resources: int

    created: list[str]
    modified: list[str]
    deleted: list[str]

    unchanged: list[str]


class CloudResourceResponse(BaseModel):
    resource_id: str
    asset_id: Optional[str]

    name: str
    resource_type: str

    provider: str
    region: str
    status: str

    configuration: str

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class CloudDeltaEventResponse(BaseModel):
    event_id: str

    resource_id: str

    change_type: str

    changed_fields: Optional[str]

    previous_state: Optional[str]

    current_state: Optional[str]

    created_at: datetime

    model_config = {
        "from_attributes": True
    }