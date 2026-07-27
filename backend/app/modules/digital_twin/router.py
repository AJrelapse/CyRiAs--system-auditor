import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.db.models import (
    DigitalTwinSnapshotDB,
)

from .models import (
    DigitalTwinGraph,
)

from .service import (
    digital_twin_service,
)

from app.db.models import (
    DigitalTwinSnapshotDB,
    DigitalTwinChangeDB,
)

from .models import (
    DigitalTwinGraph,
    TwinSyncResult,
    TwinChangeResponse,
)


router = APIRouter(

    prefix="/digital-twin",

    tags=[
        "Digital Twin"
    ],
)


@router.post(
    "/build",
    response_model=DigitalTwinGraph,
)
def build_digital_twin(

    db: Session = Depends(
        get_db
    ),

):

    return (
        digital_twin_service
        .build_twin(db)
    )


@router.get(
    "/current",
    response_model=DigitalTwinGraph,
)
def get_current_twin():

    return (
        digital_twin_service
        .export_graph()
    )


@router.get(
    "/snapshots",
)
def get_twin_snapshots(

    db: Session = Depends(
        get_db
    ),

):

    snapshots = (

        db.query(
            DigitalTwinSnapshotDB
        )

        .order_by(
            DigitalTwinSnapshotDB
            .created_at
            .desc()
        )

        .all()
    )


    return [

        {
            "snapshot_id":
                snapshot.snapshot_id,

            "node_count":
                snapshot.node_count,

            "edge_count":
                snapshot.edge_count,

            "created_at":
                snapshot.created_at,
        }

        for snapshot
        in snapshots
    ]

@router.post(
    "/synchronize",
    response_model=TwinSyncResult,
)
def synchronize_digital_twin(
    db: Session = Depends(get_db),
):

    return (
        digital_twin_service
        .synchronize_incrementally(db)
    )


@router.get(
    "/changes",
    response_model=list[
        TwinChangeResponse
    ],
)
def get_digital_twin_changes(
    db: Session = Depends(get_db),
):

    return (

        db.query(
            DigitalTwinChangeDB
        )

        .order_by(
            DigitalTwinChangeDB
            .created_at
            .desc()
        )

        .all()
    )