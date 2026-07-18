from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel


class AssetConfiguration(BaseModel):

    asset_id: str

    hostname: Optional[str] = None

    operating_system: Optional[str] = None

    os_version: Optional[str] = None

    patch_level: Optional[str] = None

    last_patch_date: Optional[datetime] = None

    open_ports: list[int] = []

    installed_software: list[dict[str, Any]] = []

    firewall_rules: list[dict[str, Any]] = []

    security_controls: list[str] = []

    configuration_metadata: dict[str, Any] = {}


class ConfigurationSyncResult(BaseModel):

    total_received: int

    added: list[str]

    updated: list[str]

    unchanged: list[str]

class AssetConfigurationResponse(BaseModel):

    asset_id: str

    hostname: Optional[str]

    operating_system: Optional[str]

    os_version: Optional[str]

    patch_level: Optional[str]

    last_patch_date: Optional[datetime]

    open_ports: str

    installed_software: str

    firewall_rules: str

    security_controls: str

    configuration_metadata: str

    created_at: datetime

    updated_at: datetime


    model_config = {
        "from_attributes": True
    }