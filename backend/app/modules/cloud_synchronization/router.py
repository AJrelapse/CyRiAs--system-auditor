from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.db.models import (
    CloudResourceDB,
    CloudDeltaEventDB,
)

from .models import (
    CloudResource,
    CloudSyncResult,
    CloudResourceResponse,
    CloudDeltaEventResponse,
)

from .service import (
    cloud_synchronization_service,
)


router = APIRouter(
    prefix="/cloud",
    tags=["Cloud Synchronization"],
)


@router.get(
    "/state",
    response_model=list[CloudResource],
)
def get_current_cloud_state():

    return (
        cloud_synchronization_service
        .collect_cloud_state()
    )


@router.post(
    "/synchronize",
    response_model=CloudSyncResult,
)
def synchronize_cloud_state(
    db: Session = Depends(get_db),
):

    return (
        cloud_synchronization_service
        .synchronize(db)
    )


@router.get(
    "/resources",
    response_model=list[
        CloudResourceResponse
    ],
)
def get_cloud_resources(
    db: Session = Depends(get_db),
):

    return (
        db.query(CloudResourceDB)
        .order_by(
            CloudResourceDB.resource_id
        )
        .all()
    )


@router.get(
    "/events",
    response_model=list[
        CloudDeltaEventResponse
    ],
)
def get_cloud_delta_events(
    db: Session = Depends(get_db),
):

    return (
        db.query(CloudDeltaEventDB)
        .order_by(
            CloudDeltaEventDB
            .created_at
            .desc()
        )
        .all()
    )