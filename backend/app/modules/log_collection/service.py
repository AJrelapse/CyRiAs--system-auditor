import json

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from sqlalchemy import func

from app.db.models import SecurityEventDB

from .mock_provider import generate_mock_logs

from .models import (
    NormalizedSecurityEvent,
    LogIngestionResult,
    LogSummaryResponse,
)


class LogCollectionService:

    def collect_logs(
        self,
    ) -> list[NormalizedSecurityEvent]:

        return generate_mock_logs()

    def get_log_summary(
        self,
        db: Session,
        window_minutes: int,
    ) -> LogSummaryResponse:

        cutoff_time = (
            datetime.now(timezone.utc)
            - timedelta(
                minutes=window_minutes
            )
        )


        events = (
            db.query(SecurityEventDB)
            .filter(
                SecurityEventDB.timestamp
                >= cutoff_time
            )
            .all()
        )


        critical_events = 0
        high_events = 0
        medium_events = 0
        failed_authentications = 0

        affected_assets = set()


        for event in events:

            if event.severity == "critical":
                critical_events += 1

            elif event.severity == "high":
                high_events += 1

            elif event.severity == "medium":
                medium_events += 1


            if (
                event.category
                == "authentication"
                and event.successful is False
            ):
                failed_authentications += 1


            if event.asset_id:

                affected_assets.add(
                    event.asset_id
                )


        return LogSummaryResponse(

            window_minutes=window_minutes,

            total_events=len(events),

            critical_events=critical_events,

            high_events=high_events,

            medium_events=medium_events,

            failed_authentications=(
                failed_authentications
            ),

            affected_assets=sorted(
                affected_assets
            ),
        )

    def ingest_logs(
        self,
        db: Session,
    ) -> LogIngestionResult:

        events = self.collect_logs()

        inserted = 0
        duplicates = 0


        for event in events:

            existing = (
                db.query(SecurityEventDB)
                .filter(
                    SecurityEventDB.event_id
                    == event.event_id
                )
                .first()
            )


            if existing:

                duplicates += 1
                continue


            database_event = SecurityEventDB(

                event_id=event.event_id,

                timestamp=event.timestamp,

                source_type=event.source_type.value,

                source_name=event.source_name,

                asset_id=event.asset_id,

                category=event.category.value,

                event_type=event.event_type,

                severity=event.severity.value,

                message=event.message,

                source_ip=event.source_ip,

                destination_ip=event.destination_ip,

                username=event.username,

                successful=event.successful,

                raw_data=json.dumps(
                    event.raw_data or {}
                ),
            )


            db.add(
                database_event
            )

            inserted += 1


        db.commit()


        return LogIngestionResult(

            total_received=len(events),

            inserted=inserted,

            duplicates=duplicates,
        )


log_collection_service = (
    LogCollectionService()
)