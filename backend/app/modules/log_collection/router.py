from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import SecurityEventDB

from .models import (
    NormalizedSecurityEvent,
    LogIngestionResult,
    SecurityEventResponse,
    LogSummaryResponse,
)

from .service import (
    log_collection_service,
)


router = APIRouter(
    prefix="/logs",
    tags=["Log Collection"],
)


@router.get(
    "/collect",
    response_model=list[
        NormalizedSecurityEvent
    ],
)
def collect_logs():

    return (
        log_collection_service
        .collect_logs()
    )


@router.post(
    "/ingest",
    response_model=LogIngestionResult,
)
def ingest_logs(
    db: Session = Depends(get_db),
):

    return (
        log_collection_service
        .ingest_logs(db)
    )


@router.get(
    "/events",
    response_model=list[
        SecurityEventResponse
    ],
)
def get_security_events(
    db: Session = Depends(get_db),
):

    return (
        db.query(SecurityEventDB)
        .order_by(
            SecurityEventDB
            .timestamp
            .desc()
        )
        .all()
    )

@router.get(
    "/summary",
    response_model=LogSummaryResponse,
)
def get_log_summary(

    window_minutes: int = Query(
        default=60,
        ge=1,
        le=1440,
    ),

    db: Session = Depends(get_db),
):

    return (
        log_collection_service
        .get_log_summary(
            db=db,
            window_minutes=window_minutes,
        )
    )