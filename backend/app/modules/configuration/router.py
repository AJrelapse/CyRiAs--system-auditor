from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.db.models import (
    AssetConfigurationDB,
)

from .models import (
    AssetConfiguration,
    ConfigurationSyncResult,
    AssetConfigurationResponse,
)

from .service import (
    configuration_collection_service,
)


router = APIRouter(
    prefix="/configurations",
    tags=["Configuration Collection"],
)


@router.get(
    "/collect",
    response_model=list[
        AssetConfiguration
    ],
)
def collect_configurations():

    return (
        configuration_collection_service
        .collect_configurations()
    )


@router.post(
    "/synchronize",
    response_model=ConfigurationSyncResult,
)
def synchronize_configurations(
    db: Session = Depends(get_db),
):

    return (
        configuration_collection_service
        .synchronize_configurations(db)
    )


@router.get(
    "/inventory",
    response_model=list[
        AssetConfigurationResponse
    ],
)
def get_configuration_inventory(
    db: Session = Depends(get_db),
):

    return (
        db.query(
            AssetConfigurationDB
        )
        .order_by(
            AssetConfigurationDB.asset_id
        )
        .all()
    )


@router.get(
    "/inventory/{asset_id}",
    response_model=AssetConfigurationResponse,
)
def get_asset_configuration(

    asset_id: str,

    db: Session = Depends(get_db),
):

    configuration = (

        db.query(
            AssetConfigurationDB
        )

        .filter(
            AssetConfigurationDB.asset_id
            == asset_id
        )

        .first()
    )


    if configuration is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "Configuration not found "
                "for asset"
            ),
        )


    return configuration