import json

from sqlalchemy.orm import Session

from app.db.models import (
    AssetDB,
    AssetConfigurationDB,
)

from .mock_provider import (
    collect_mock_configurations,
)

from .models import (
    AssetConfiguration,
    ConfigurationSyncResult,
)


class ConfigurationCollectionService:

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

                    asset_id=(
                        configuration.asset_id
                    ),

                    **serialized_values,
                )


                db.add(stored)

                added.append(
                    configuration.asset_id
                )

                continue


            # -------------------------
            # Detect configuration delta
            # -------------------------

            changed = False


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

                    changed = True


            if changed:

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