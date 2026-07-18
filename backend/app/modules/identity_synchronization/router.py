from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.db.models import (
    IdentityDB,
    IdentityDeltaEventDB,
)

from .models import (
    Identity,
    IdentitySyncResult,
    IdentityResponse,
    IdentityDeltaEventResponse,
)

from .service import (
    identity_synchronization_service,
)


router = APIRouter(

    prefix="/identities",

    tags=[
        "Identity Synchronization"
    ],
)


@router.get(
    "/state",
    response_model=list[Identity],
)
def get_identity_state():

    return (
        identity_synchronization_service
        .collect_identity_state()
    )


@router.post(
    "/synchronize",
    response_model=IdentitySyncResult,
)
def synchronize_identity_state(

    db: Session = Depends(
        get_db
    ),

):

    return (
        identity_synchronization_service
        .synchronize(db)
    )


@router.get(
    "/inventory",
    response_model=list[
        IdentityResponse
    ],
)
def get_identity_inventory(

    db: Session = Depends(
        get_db
    ),

):

    return (

        db.query(
            IdentityDB
        )

        .order_by(
            IdentityDB.identity_id
        )

        .all()
    )


@router.get(
    "/events",
    response_model=list[
        IdentityDeltaEventResponse
    ],
)
def get_identity_events(

    db: Session = Depends(
        get_db
    ),

):

    return (

        db.query(
            IdentityDeltaEventDB
        )

        .order_by(
            IdentityDeltaEventDB
            .created_at
            .desc()
        )

        .all()
    )