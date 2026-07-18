import json

from sqlalchemy.orm import Session

from app.db.models import (
    AssetDB,
    AssetChangeEventDB,
)

from .mock_provider import discover_mock_assets
from .models import Asset, DiscoveryResult


class AssetDiscoveryService:

    def discover_assets(self) -> list[Asset]:

        return discover_mock_assets()


    def create_change_event(
        self,
        db: Session,
        asset_id: str,
        change_type: str,
        changed_fields: list[str] | None = None,
    ):

        event = AssetChangeEventDB(
            asset_id=asset_id,
            change_type=change_type,
            changed_fields=json.dumps(
                changed_fields or []
            ),
        )

        db.add(event)


    def synchronize_inventory(
        self,
        db: Session,
    ) -> DiscoveryResult:

        discovered_assets = self.discover_assets()

        stored_assets = db.query(
            AssetDB
        ).all()


        stored_by_id = {
            asset.asset_id: asset
            for asset in stored_assets
        }


        discovered_by_id = {
            asset.asset_id: asset
            for asset in discovered_assets
        }


        added = []
        updated = []
        removed = []


        # --------------------------------
        # Detect added and updated assets
        # --------------------------------

        for asset_id, discovered in discovered_by_id.items():

            stored = stored_by_id.get(
                asset_id
            )


            # New asset
            if stored is None:

                new_asset = AssetDB(
                    asset_id=discovered.asset_id,
                    name=discovered.name,
                    asset_type=discovered.asset_type.value,
                    ip_address=discovered.ip_address,
                    operating_system=discovered.operating_system,
                    owner=discovered.owner,
                    environment=discovered.environment.value,
                    criticality=discovered.criticality.value,
                    provider=discovered.provider,
                    region=discovered.region,
                    status=discovered.status,
                )

                db.add(new_asset)


                self.create_change_event(
                    db=db,
                    asset_id=asset_id,
                    change_type="ADDED",
                )


                added.append(
                    asset_id
                )

                continue


            fields_to_compare = {

                "name":
                    discovered.name,

                "asset_type":
                    discovered.asset_type.value,

                "ip_address":
                    discovered.ip_address,

                "operating_system":
                    discovered.operating_system,

                "owner":
                    discovered.owner,

                "environment":
                    discovered.environment.value,

                "criticality":
                    discovered.criticality.value,

                "provider":
                    discovered.provider,

                "region":
                    discovered.region,

                "status":
                    discovered.status,
            }


            changed_fields = []


            for (
                field_name,
                new_value
            ) in fields_to_compare.items():

                old_value = getattr(
                    stored,
                    field_name,
                )


                if old_value != new_value:

                    setattr(
                        stored,
                        field_name,
                        new_value,
                    )

                    changed_fields.append(
                        field_name
                    )


            if changed_fields:

                self.create_change_event(
                    db=db,
                    asset_id=asset_id,
                    change_type="UPDATED",
                    changed_fields=changed_fields,
                )


                updated.append(
                    asset_id
                )


        # -------------------------
        # Detect removed assets
        # -------------------------

        for (
            asset_id,
            stored
        ) in stored_by_id.items():

            if asset_id not in discovered_by_id:

                # Avoid repeatedly generating
                # REMOVED events.
                if stored.status != "removed":

                    stored.status = "removed"


                    self.create_change_event(
                        db=db,
                        asset_id=asset_id,
                        change_type="REMOVED",
                        changed_fields=[
                            "status"
                        ],
                    )


                    removed.append(
                        asset_id
                    )


        db.commit()


        return DiscoveryResult(
            total_discovered=len(
                discovered_assets
            ),
            added=added,
            updated=updated,
            removed=removed,
        )


asset_discovery_service = (
    AssetDiscoveryService()
)