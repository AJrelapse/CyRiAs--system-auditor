from datetime import datetime, timezone
from uuid import uuid4

from .models import (
    NormalizedSecurityEvent,
    LogSourceType,
    EventSeverity,
    EventCategory,
)


def generate_mock_logs() -> list[NormalizedSecurityEvent]:

    now = datetime.now(timezone.utc)

    events = [

        # Normal successful login
        NormalizedSecurityEvent(
            event_id=str(uuid4()),
            timestamp=now,
            source_type=LogSourceType.IDENTITY,
            source_name="Corporate Identity Provider",
            asset_id="SRV-002",
            category=EventCategory.AUTHENTICATION,
            event_type="LOGIN_SUCCESS",
            severity=EventSeverity.INFO,
            message="Successful employee authentication",
            source_ip="10.0.10.50",
            destination_ip="10.0.1.20",
            username="finance.user",
            successful=True,
            raw_data={
                "authentication_method": "password"
            },
        ),

        # Failed login attempt
        NormalizedSecurityEvent(
            event_id=str(uuid4()),
            timestamp=now,
            source_type=LogSourceType.IDENTITY,
            source_name="Corporate Identity Provider",
            asset_id="SRV-002",
            category=EventCategory.AUTHENTICATION,
            event_type="LOGIN_FAILED",
            severity=EventSeverity.MEDIUM,
            message="Failed authentication attempt",
            source_ip="198.51.100.25",
            destination_ip="10.0.1.20",
            username="admin",
            successful=False,
            raw_data={
                "reason": "invalid_password"
            },
        ),

        # Suspicious external connection
        NormalizedSecurityEvent(
            event_id=str(uuid4()),
            timestamp=now,
            source_type=LogSourceType.NETWORK,
            source_name="Enterprise Firewall",
            asset_id="SRV-001",
            category=EventCategory.NETWORK_CONNECTION,
            event_type="INBOUND_CONNECTION",
            severity=EventSeverity.HIGH,
            message=(
                "Suspicious inbound connection "
                "detected on public web server"
            ),
            source_ip="198.51.100.70",
            destination_ip="203.0.113.10",
            successful=True,
            raw_data={
                "destination_port": 443,
                "protocol": "TCP"
            },
        ),

        # Application event
        NormalizedSecurityEvent(
            event_id=str(uuid4()),
            timestamp=now,
            source_type=LogSourceType.APPLICATION,
            source_name="Customer Web Application",
            asset_id="APP-001",
            category=EventCategory.APPLICATION_ACTIVITY,
            event_type="API_REQUEST",
            severity=EventSeverity.INFO,
            message="Customer API request processed",
            source_ip="203.0.113.25",
            destination_ip="203.0.113.10",
            successful=True,
            raw_data={
                "endpoint": "/api/customers",
                "method": "GET",
                "status_code": 200
            },
        ),

        # Malware detection
        NormalizedSecurityEvent(
            event_id=str(uuid4()),
            timestamp=now,
            source_type=LogSourceType.SECURITY,
            source_name="Endpoint Detection Platform",
            asset_id="END-001",
            category=EventCategory.MALWARE,
            event_type="MALWARE_DETECTED",
            severity=EventSeverity.CRITICAL,
            message=(
                "Potential malware detected "
                "on finance workstation"
            ),
            source_ip="10.0.10.50",
            username="finance.user",
            successful=None,
            raw_data={
                "malware_family": "DemoRansomware",
                "action": "quarantined"
            },
        ),

    ]

    return events