from datetime import datetime
from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel, Field


class LogSourceType(str, Enum):
    SYSTEM = "system"
    APPLICATION = "application"
    NETWORK = "network"
    SECURITY = "security"
    IDENTITY = "identity"


class EventSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EventCategory(str, Enum):
    AUTHENTICATION = "authentication"
    NETWORK_CONNECTION = "network_connection"
    APPLICATION_ACTIVITY = "application_activity"
    SYSTEM_ACTIVITY = "system_activity"
    MALWARE = "malware"
    PRIVILEGE_CHANGE = "privilege_change"
    VULNERABILITY = "vulnerability"
    OTHER = "other"


class NormalizedSecurityEvent(BaseModel):

    event_id: str

    timestamp: datetime

    source_type: LogSourceType

    source_name: str

    asset_id: Optional[str] = None

    category: EventCategory

    event_type: str

    severity: EventSeverity

    message: str

    source_ip: Optional[str] = None

    destination_ip: Optional[str] = None

    username: Optional[str] = None

    successful: Optional[bool] = None

    raw_data: Optional[dict[str, Any]] = None


class LogIngestionResult(BaseModel):

    total_received: int

    inserted: int

    duplicates: int

class SecurityEventResponse(BaseModel):

    event_id: str

    timestamp: datetime

    source_type: str

    source_name: str

    asset_id: Optional[str]

    category: str

    event_type: str

    severity: str

    message: str

    source_ip: Optional[str]

    destination_ip: Optional[str]

    username: Optional[str]

    successful: Optional[bool]

    raw_data: Optional[str]

    ingested_at: datetime


    model_config = {
        "from_attributes": True
    }

class LogSummaryResponse(BaseModel):

    window_minutes: int

    total_events: int

    critical_events: int

    high_events: int

    medium_events: int

    failed_authentications: int

    affected_assets: list[str]