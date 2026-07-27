import json

from sqlalchemy.orm import Session

from app.db.models import (
    AssetDB,
    AssetConfigurationDB,
    ConfigurationDeltaEventDB,
)

from .mock_provider import (
    collect_mock_configurations,
)

from .models import (
    AssetConfiguration,
    ConfigurationSyncResult,
)


class ConfigurationCollectionService:
    def create_delta_event(
        self,
        db: Session,
        asset_id: str,
        change_type: str,
        changed_fields: list[str],
        previous_state: dict | None,
        current_state: dict | None,
    ):

        event = ConfigurationDeltaEventDB(

            asset_id=asset_id,

            change_type=change_type,

            changed_fields=json.dumps(
                changed_fields
            ),

            previous_state=(
                json.dumps(
                    previous_state,
                    default=str,
                )
                if previous_state
                is not None
                else None
            ),

            current_state=(
                json.dumps(
                    current_state,
                    default=str,
                )
                if current_state
                is not None
                else None
            ),
        )

        db.add(event)

    def collect_configurations(
        self,
    ) -> list[AssetConfiguration]:

        return collect_mock_configurations()


    def synchronize_configurations(
        self,
        db: Session,
    ) -> ConfigurationSyncResult:

        configurations = (
            self.collect_configurations()
        )

        added = []
        updated = []
        unchanged = []


        for configuration in configurations:

            # Verify that Module 1 knows this asset

            asset = (
                db.query(AssetDB)
                .filter(
                    AssetDB.asset_id
                    == configuration.asset_id
                )
                .first()
            )


            if asset is None:

                continue


            serialized_values = {

                "hostname":
                    configuration.hostname,

                "operating_system":
                    configuration.operating_system,

                "os_version":
                    configuration.os_version,

                "patch_level":
                    configuration.patch_level,

                "last_patch_date":
                    configuration.last_patch_date,

                "open_ports":
                    json.dumps(
                        configuration.open_ports
                    ),

                "installed_software":
                    json.dumps(
                        configuration.installed_software
                    ),

                "firewall_rules":
                    json.dumps(
                        configuration.firewall_rules
                    ),

                "security_controls":
                    json.dumps(
                        configuration.security_controls
                    ),

                "configuration_metadata":
                    json.dumps(
                        configuration
                        .configuration_metadata
                    ),
            }


            stored = (
                db.query(
                    AssetConfigurationDB
                )
                .filter(
                    AssetConfigurationDB.asset_id
                    == configuration.asset_id
                )
                .first()
            )


            # -------------------------
            # New configuration
            # -------------------------

            if stored is None:

                stored = AssetConfigurationDB(
                    asset_id=configuration.asset_id,
                    **serialized_values,
                )

                db.add(stored)


                self.create_delta_event(

                    db=db,

                    asset_id=configuration.asset_id,

                    change_type="CREATED",

                    changed_fields=list(
                        serialized_values.keys()
                    ),

                    previous_state=None,

                    current_state=serialized_values,
                )


                added.append(
                    configuration.asset_id
                )

                continue


            # -------------------------
            # Detect configuration delta
            # -------------------------

            previous_state = {

                field_name:
                    getattr(
                        stored,
                        field_name,
                    )

                for field_name
                in serialized_values
            }


            changed_fields = []


            for (
                field_name,
                new_value
            ) in serialized_values.items():

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

                self.create_delta_event(

                    db=db,

                    asset_id=(
                        configuration.asset_id
                    ),

                    change_type="MODIFIED",

                    changed_fields=(
                        changed_fields
                    ),

                    previous_state=(
                        previous_state
                    ),

                    current_state=(
                        serialized_values
                    ),
                )


                updated.append(
                    configuration.asset_id
                )

            else:

                unchanged.append(
                    configuration.asset_id
                )


        db.commit()


        return ConfigurationSyncResult(

            total_received=len(
                configurations
            ),

            added=added,

            updated=updated,

            unchanged=unchanged,
        )


configuration_collection_service = (
    ConfigurationCollectionService()
)