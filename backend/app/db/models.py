from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AssetDB(Base):

    __tablename__ = "assets"

    asset_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    asset_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    operating_system: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    owner: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    environment: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    criticality: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    provider: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    region: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="active",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

class AssetChangeEventDB(Base):

    __tablename__ = "asset_change_events"

    event_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    asset_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    change_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    changed_fields: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

class SecurityEventDB(Base):

    __tablename__ = "security_events"

    event_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    source_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    source_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    asset_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    message: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    source_ip: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    destination_ip: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    username: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    successful: Mapped[bool | None] = mapped_column(
        nullable=True,
    )

    raw_data: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    ingested_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

class AssetConfigurationDB(Base):

    __tablename__ = "asset_configurations"

    asset_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    hostname: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    operating_system: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    os_version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    patch_level: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    last_patch_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    open_ports: Mapped[str] = mapped_column(
        String,
        default="[]",
    )

    installed_software: Mapped[str] = mapped_column(
        String,
        default="[]",
    )

    firewall_rules: Mapped[str] = mapped_column(
        String,
        default="[]",
    )

    security_controls: Mapped[str] = mapped_column(
        String,
        default="[]",
    )

    configuration_metadata: Mapped[str] = mapped_column(
        String,
        default="{}",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

class CloudResourceDB(Base):

    __tablename__ = "cloud_resources"

    resource_id: Mapped[str] = mapped_column(
        String(150),
        primary_key=True,
    )

    asset_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    resource_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    region: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="active",
    )

    configuration: Mapped[str] = mapped_column(
        String,
        default="{}",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class CloudDeltaEventDB(Base):

    __tablename__ = "cloud_delta_events"

    event_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    resource_id: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    change_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    changed_fields: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    previous_state: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    current_state: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )

class IdentityDB(Base):

    __tablename__ = "identities"

    identity_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    identity_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    department: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="active",
    )

    groups: Mapped[str] = mapped_column(
        String,
        default="[]",
    )

    roles: Mapped[str] = mapped_column(
        String,
        default="[]",
    )

    direct_permissions: Mapped[str] = mapped_column(
        String,
        default="[]",
    )

    effective_permissions: Mapped[str] = mapped_column(
        String,
        default="[]",
    )

    accessible_assets: Mapped[str] = mapped_column(
        String,
        default="[]",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class IdentityDeltaEventDB(Base):

    __tablename__ = "identity_delta_events"

    event_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    identity_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    change_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    changed_fields: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    previous_state: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    current_state: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )

class DigitalTwinSnapshotDB(Base):

    __tablename__ = "digital_twin_snapshots"

    snapshot_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    node_count: Mapped[int] = mapped_column(
        nullable=False,
    )

    edge_count: Mapped[int] = mapped_column(
        nullable=False,
    )

    graph_data: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )


class DigitalTwinChangeDB(Base):

    __tablename__ = "digital_twin_changes"

    change_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    entity_id: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    entity_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    change_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    source_module: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    details: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

class TwinProcessedEventDB(Base):

    __tablename__ = "twin_processed_events"

    processed_event_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    source_event_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    source_module: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    processed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

class ConfigurationDeltaEventDB(Base):

    __tablename__ = "configuration_delta_events"

    event_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    asset_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    change_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    changed_fields: Mapped[str] = mapped_column(
        String,
        default="[]",
    )

    previous_state: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    current_state: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )

class VulnerabilityDB(Base):

    __tablename__ = "vulnerabilities"

    vulnerability_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    cve_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    cvss_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    affected_products: Mapped[str] = mapped_column(
        Text,
        default="[]",
    )

    published_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

class ThreatTechniqueDB(Base):

    __tablename__ = "threat_techniques"

    technique_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    mitre_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    tactic: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

class SecurityControlDB(Base):

    __tablename__ = "security_controls"

    control_id: Mapped[str] = mapped_column(
       String(100),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    implementation_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )