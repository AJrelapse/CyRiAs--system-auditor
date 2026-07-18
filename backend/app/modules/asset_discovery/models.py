from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime

class AssetType(str, Enum):
    SERVER = "server"
    DATABASE = "database"
    APPLICATION = "application"
    ENDPOINT = "endpoint"
    CLOUD_RESOURCE = "cloud_resource"


class EnvironmentType(str, Enum):
    PRODUCTION = "production"
    DEVELOPMENT = "development"
    TESTING = "testing"


class CriticalityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Asset(BaseModel):
    asset_id: str = Field(
        ...,
        description="Unique identifier of the enterprise asset"
    )

    name: str

    asset_type: AssetType

    ip_address: Optional[str] = None

    operating_system: Optional[str] = None

    owner: Optional[str] = None

    environment: EnvironmentType

    criticality: CriticalityLevel

    provider: Optional[str] = None

    region: Optional[str] = None

    status: str = "active"

class AssetChange(BaseModel):
    asset_id: str
    change_type: str


class DiscoveryResult(BaseModel):
    total_discovered: int
    added: list[str]
    updated: list[str]
    removed: list[str]

class AssetInventoryResponse(BaseModel):

    asset_id: str
    name: str
    asset_type: str
    ip_address: Optional[str]
    operating_system: Optional[str]
    owner: Optional[str]
    environment: str
    criticality: str
    provider: Optional[str]
    region: Optional[str]
    status: str

    model_config = {
        "from_attributes": True
    }


class AssetChangeEventResponse(BaseModel):

    event_id: str
    asset_id: str
    change_type: str
    changed_fields: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }