from datetime import datetime, timezone

from .models import AssetConfiguration


def collect_mock_configurations() -> list[AssetConfiguration]:

    return [

        # ---------------------------------
        # Public Web Server
        # ---------------------------------

        AssetConfiguration(

            asset_id="SRV-001",

            hostname="web-prod-01",

            operating_system="Ubuntu",

            os_version="22.04",

            patch_level="2026-06",

            last_patch_date=datetime(
                2026,
                6,
                10,
                tzinfo=timezone.utc,
            ),

            open_ports=[
                22,
                80,
                443,
            ],

            installed_software=[

                {
                    "name": "nginx",
                    "version": "1.22.0",
                },

                {
                    "name": "OpenSSH",
                    "version": "8.9",
                },

            ],

            firewall_rules=[

                {
                    "source": "0.0.0.0/0",
                    "destination_port": 80,
                    "protocol": "TCP",
                    "action": "ALLOW",
                },

                {
                    "source": "0.0.0.0/0",
                    "destination_port": 443,
                    "protocol": "TCP",
                    "action": "ALLOW",
                },

                # Intentionally risky
                {
                    "source": "0.0.0.0/0",
                    "destination_port": 22,
                    "protocol": "TCP",
                    "action": "ALLOW",
                },

            ],

            security_controls=[
                "firewall",
                "endpoint_monitoring",
            ],

            configuration_metadata={
                "publicly_accessible": True,
            },
        ),


        # ---------------------------------
        # Customer Application
        # ---------------------------------

        AssetConfiguration(

            asset_id="APP-001",

            hostname="customer-app-prod",

            operating_system="Linux",

            os_version="22.04",

            patch_level="2026-07",

            last_patch_date=datetime(
                2026,
                7,
                1,
                tzinfo=timezone.utc,
            ),

            open_ports=[
                8080,
            ],

            installed_software=[

                {
                    "name": "Python",
                    "version": "3.11",
                },

                {
                    "name": "FastAPI",
                    "version": "0.115",
                },

            ],

            firewall_rules=[

                {
                    "source": "SRV-001",
                    "destination_port": 8080,
                    "protocol": "TCP",
                    "action": "ALLOW",
                }

            ],

            security_controls=[
                "application_logging",
                "input_validation",
            ],

            configuration_metadata={
                "publicly_accessible": False,
            },
        ),


        # ---------------------------------
        # Customer Database
        # ---------------------------------

        AssetConfiguration(

            asset_id="DB-001",

            hostname="customer-db-prod",

            operating_system="Linux",

            os_version="22.04",

            patch_level="2026-05",

            last_patch_date=datetime(
                2026,
                5,
                15,
                tzinfo=timezone.utc,
            ),

            open_ports=[
                5432,
            ],

            installed_software=[

                {
                    "name": "PostgreSQL",
                    "version": "16",
                }

            ],

            firewall_rules=[

                {
                    "source": "APP-001",
                    "destination_port": 5432,
                    "protocol": "TCP",
                    "action": "ALLOW",
                }

            ],

            security_controls=[
                "database_encryption",
                "backup",
            ],

            configuration_metadata={
                "contains_sensitive_data": True,
            },
        ),


        # ---------------------------------
        # Authentication Server
        # ---------------------------------

        AssetConfiguration(

            asset_id="SRV-002",

            hostname="auth-server-01",

            operating_system="Windows Server",

            os_version="2022",

            patch_level="2026-06",

            last_patch_date=datetime(
                2026,
                6,
                20,
                tzinfo=timezone.utc,
            ),

            open_ports=[
                389,
                636,
            ],

            installed_software=[

                {
                    "name": "Directory Service",
                    "version": "2022",
                }

            ],

            firewall_rules=[],

            security_controls=[
                "mfa",
                "privileged_access_monitoring",
            ],

            configuration_metadata={
                "identity_provider": True,
            },
        ),


        # ---------------------------------
        # Finance Workstation
        # ---------------------------------

        AssetConfiguration(

            asset_id="END-001",

            hostname="finance-ws-01",

            operating_system="Windows",

            os_version="11",

            patch_level="2026-07",

            last_patch_date=datetime(
                2026,
                7,
                5,
                tzinfo=timezone.utc,
            ),

            open_ports=[],

            installed_software=[

                {
                    "name": "Microsoft Office",
                    "version": "2024",
                }

            ],

            firewall_rules=[],

            security_controls=[
                "antivirus",
                "endpoint_detection",
            ],

            configuration_metadata={
                "department": "finance",
            },
        ),

    ]