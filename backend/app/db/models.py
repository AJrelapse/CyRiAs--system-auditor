from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String
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