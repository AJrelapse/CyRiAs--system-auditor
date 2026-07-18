import json

from sqlalchemy.orm import Session

from app.db.models import (
    CloudResourceDB,
    CloudDeltaEventDB,
)

from .mock_provider import (
    get_mock_cloud_resources,
)

from .models import (
    CloudResource,
    CloudSyncResult,
)


class CloudSynchronizationService:

    def collect_cloud_state(
        self,
    ) -> list[CloudResource]:

        return get_mock_cloud_resources()


    def create_delta_event(
        self,
        db: Session,
        resource_id: str,
        change_type: str,
        changed_fields: list[str],
        previous_state: dict | None,
        current_state: dict | None,
    ):

        event = CloudDeltaEventDB(
            resource_id=resource_id,
            change_type=change_type,

            changed_fields=json.dumps(
                changed_fields
            ),

            previous_state=(
                json.dumps(previous_state)
                if previous_state
                is not None
                else None
            ),

            current_state=(
                json.dumps(current_state)
                if current_state
                is not None
                else None
            ),
        )

        db.add(event)


    def serialize_resource(
        self,
        resource: CloudResource,
    ) -> dict:

        return {
            "asset_id":
                resource.asset_id,

            "name":
                resource.name,

            "resource_type":
                resource.resource_type.value,

            "provider":
                resource.provider,

            "region":
                resource.region,

            "status":
                resource.status,

            "configuration":
                json.dumps(
                    resource.configuration,
                    sort_keys=True,
                ),
        }


    def database_state(
        self,
        resource: CloudResourceDB,
    ) -> dict:

        return {
            "asset_id":
                resource.asset_id,

            "name":
                resource.name,

            "resource_type":
                resource.resource_type,

            "provider":
                resource.provider,

            "region":
                resource.region,

            "status":
                resource.status,

            "configuration":
                resource.configuration,
        }


    def synchronize(
        self,
        db: Session,
    ) -> CloudSyncResult:

        current_resources = (
            self.collect_cloud_state()
        )

        stored_resources = (
            db.query(CloudResourceDB)
            .all()
        )


        current_by_id = {
            resource.resource_id:
                resource
            for resource
            in current_resources
        }


        stored_by_id = {
            resource.resource_id:
                resource
            for resource
            in stored_resources
        }


        created = []
        modified = []
        deleted = []
        unchanged = []


        # -------------------------
        # CREATED / MODIFIED
        # -------------------------

        for (
            resource_id,
            current
        ) in current_by_id.items():

            stored = stored_by_id.get(
                resource_id
            )

            current_state = (
                self.serialize_resource(
                    current
                )
            )


            if stored is None:

                new_resource = (
                    CloudResourceDB(
                        resource_id=resource_id,
                        **current_state,
                    )
                )

                db.add(new_resource)


                self.create_delta_event(
                    db=db,

                    resource_id=resource_id,

                    change_type="CREATED",

                    changed_fields=list(
                        current_state.keys()
                    ),

                    previous_state=None,

                    current_state=(
                        current_state
                    ),
                )


                created.append(
                    resource_id
                )

                continue


            previous_state = (
                self.database_state(
                    stored
                )
            )


            changed_fields = []


            for (
                field_name,
                new_value
            ) in current_state.items():

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

                    resource_id=resource_id,

                    change_type="MODIFIED",

                    changed_fields=(
                        changed_fields
                    ),

                    previous_state=(
                        previous_state
                    ),

                    current_state=(
                        current_state
                    ),
                )


                modified.append(
                    resource_id
                )

            else:

                unchanged.append(
                    resource_id
                )


        # -------------------------
        # DELETED
        # -------------------------

        for (
            resource_id,
            stored
        ) in stored_by_id.items():

            if (
                resource_id
                not in current_by_id
                and stored.status
                != "deleted"
            ):

                previous_state = (
                    self.database_state(
                        stored
                    )
                )


                stored.status = "deleted"


                current_state = (
                    self.database_state(
                        stored
                    )
                )


                self.create_delta_event(
                    db=db,

                    resource_id=resource_id,

                    change_type="DELETED",

                    changed_fields=[
                        "status"
                    ],

                    previous_state=(
                        previous_state
                    ),

                    current_state=(
                        current_state
                    ),
                )


                deleted.append(
                    resource_id
                )


        db.commit()


        return CloudSyncResult(

            total_resources=len(
                current_resources
            ),

            created=created,

            modified=modified,

            deleted=deleted,

            unchanged=unchanged,
        )


cloud_synchronization_service = (
    CloudSynchronizationService()
)