from .models import (
    Asset,
    AssetType,
    EnvironmentType,
    CriticalityLevel,
)


def discover_mock_assets() -> list[Asset]:

    assets = [

        Asset(
            asset_id="SRV-001",
            name="Public Web Server",
            asset_type=AssetType.SERVER,
            ip_address="203.0.113.10",
            operating_system="Ubuntu 22.04",
            owner="Web Platform Team",
            environment=EnvironmentType.PRODUCTION,
            criticality=CriticalityLevel.HIGH,
            provider="AWS",
            region="ap-south-1",
        ),

        Asset(
            asset_id="APP-001",
            name="Customer Web Application",
            asset_type=AssetType.APPLICATION,
            owner="Application Team",
            environment=EnvironmentType.PRODUCTION,
            criticality=CriticalityLevel.HIGH,
            provider="AWS",
            region="ap-south-1",
        ),

        Asset(
            asset_id="DB-001",
            name="Customer Database",
            asset_type=AssetType.DATABASE,
            ip_address="10.0.2.15",
            operating_system="PostgreSQL 16",
            owner="Database Team",
            environment=EnvironmentType.PRODUCTION,
            criticality=CriticalityLevel.CRITICAL,
            provider="AWS",
            region="ap-south-1",
        ),

        Asset(
            asset_id="SRV-002",
            name="Internal Authentication Server",
            asset_type=AssetType.SERVER,
            ip_address="10.0.1.20",
            operating_system="Windows Server 2022",
            owner="Identity Team",
            environment=EnvironmentType.PRODUCTION,
            criticality=CriticalityLevel.CRITICAL,
            provider="On-Premise",
            region="Vellore-DC",
        ),

        Asset(
            asset_id="END-001",
            name="Finance Employee Workstation",
            asset_type=AssetType.ENDPOINT,
            ip_address="10.0.10.50",
            operating_system="Windows 11",
            owner="Finance Department",
            environment=EnvironmentType.PRODUCTION,
            criticality=CriticalityLevel.MEDIUM,
            provider="Corporate Network",
            region="Vellore-Office",
        ),

    ]

    return assets