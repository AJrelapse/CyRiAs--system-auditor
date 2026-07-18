from .models import (
    CloudResource,
    CloudResourceType,
)


def get_mock_cloud_resources() -> list[CloudResource]:

    return [

        CloudResource(
            resource_id="AWS-EC2-001",
            asset_id="SRV-001",
            name="Public Web Server",
            resource_type=(
                CloudResourceType
                .VIRTUAL_MACHINE
            ),
            provider="AWS",
            region="ap-south-1",
            configuration={
                "instance_type": "t3.medium",
                "public_ip": "203.0.113.10",
                "vpc": "production-vpc",
                "security_group": "SG-WEB-001",
            },
        ),

        CloudResource(
            resource_id="AWS-RDS-001",
            asset_id="DB-001",
            name="Customer Database",
            resource_type=(
                CloudResourceType.DATABASE
            ),
            provider="AWS",
            region="ap-south-1",
            configuration={
                "engine": "postgresql",
                "engine_version": "16",
                "publicly_accessible": False,
                "encrypted": True,
                "security_group": "SG-DB-001",
            },
        ),

        CloudResource(
            resource_id="AWS-SG-WEB-001",
            asset_id="SRV-001",
            name="Web Server Security Group",
            resource_type=(
                CloudResourceType
                .SECURITY_GROUP
            ),
            provider="AWS",
            region="ap-south-1",
            configuration={
                "inbound_rules": [
                    {
                        "protocol": "TCP",
                        "port": 80,
                        "source": "0.0.0.0/0",
                    },
                    {
                        "protocol": "TCP",
                        "port": 443,
                        "source": "0.0.0.0/0",
                    },
                    {
                        "protocol": "TCP",
                        "port": 22,
                        "source": "0.0.0.0/0",
                    },
                ]
            },
        ),

        CloudResource(
            resource_id="AWS-SG-DB-001",
            asset_id="DB-001",
            name="Database Security Group",
            resource_type=(
                CloudResourceType
                .SECURITY_GROUP
            ),
            provider="AWS",
            region="ap-south-1",
            configuration={
                "inbound_rules": [
                    {
                        "protocol": "TCP",
                        "port": 5432,
                        "source_asset": "APP-001",
                    }
                ]
            },
        ),

        CloudResource(
            resource_id="AWS-IAM-001",
            asset_id=None,
            name="Application Database Role",
            resource_type=(
                CloudResourceType.IAM_ROLE
            ),
            provider="AWS",
            region="global",
            configuration={
                "principal_asset": "APP-001",
                "permissions": [
                    "database:connect",
                    "database:read",
                ],
                "target_asset": "DB-001",
            },
        ),

    ]