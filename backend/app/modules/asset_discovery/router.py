from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.db.models import (
    AssetDB,
    AssetChangeEventDB,
)

from .models import (
    Asset,
    DiscoveryResult,
    AssetInventoryResponse,
    AssetChangeEventResponse,
)

from .service import (
    asset_discovery_service,
)


router = APIRouter(
    prefix="/assets",
    tags=[
        "Enterprise Asset Discovery"
    ],
)


# --------------------------------
# Discover current provider assets
# --------------------------------

@router.get(
    "/discover",
    response_model=list[Asset],
)
def discover_assets():

    return (
        asset_discovery_service
        .discover_assets()
    )


# --------------------------------
# Synchronize provider -> database
# --------------------------------

@router.post(
    "/synchronize",
    response_model=DiscoveryResult,
)
def synchronize_assets(
    db: Session = Depends(get_db),
):

    return (
        asset_discovery_service
        .synchronize_inventory(db)
    )


# --------------------------------
# Get complete asset inventory
# --------------------------------

@router.get(
    "/inventory",
    response_model=list[
        AssetInventoryResponse
    ],
)
def get_asset_inventory(
    db: Session = Depends(get_db),
):

    return (
        db.query(AssetDB)
        .order_by(AssetDB.asset_id)
        .all()
    )


# --------------------------------
# Get individual asset
# --------------------------------

@router.get(
    "/inventory/{asset_id}",
    response_model=AssetInventoryResponse,
)
def get_asset(
    asset_id: str,
    db: Session = Depends(get_db),
):

    asset = (
        db.query(AssetDB)
        .filter(
            AssetDB.asset_id
            == asset_id
        )
        .first()
    )


    if asset is None:

        raise HTTPException(
            status_code=404,
            detail="Asset not found",
        )


    return asset


# --------------------------------
# Get asset change-event history
# --------------------------------

@router.get(
    "/events",
    response_model=list[
        AssetChangeEventResponse
    ],
)
def get_asset_events(
    db: Session = Depends(get_db),
):

    return (
        db.query(
            AssetChangeEventDB
        )
        .order_by(
            AssetChangeEventDB
            .created_at
            .desc()
        )
        .all()
    )