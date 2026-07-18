import json

from sqlalchemy.orm import Session

from app.db.models import (
    IdentityDB,
    IdentityDeltaEventDB,
)

from .mock_provider import (
    get_mock_identities,
)

from .models import (
    Identity,
    IdentitySyncResult,
)


class IdentitySynchronizationService:


    def collect_identity_state(
        self,
    ) -> list[Identity]:

        return get_mock_identities()


    def serialize_identity(
        self,
        identity: Identity,
    ) -> dict:

        return {

            "name":
                identity.name,

            "identity_type":
                identity.identity_type.value,

            "email":
                identity.email,

            "department":
                identity.department,

            "status":
                identity.status.value,

            "groups":
                json.dumps(
                    identity.groups,
                    sort_keys=True,
                ),

            "roles":
                json.dumps(
                    identity.roles,
                    sort_keys=True,
                ),

            "direct_permissions":
                json.dumps(
                    identity.direct_permissions,
                    sort_keys=True,
                ),

            "effective_permissions":
                json.dumps(
                    identity.effective_permissions,
                    sort_keys=True,
                ),

            "accessible_assets":
                json.dumps(
                    identity.accessible_assets,
                    sort_keys=True,
                ),
        }


    def database_state(
        self,
        identity: IdentityDB,
    ) -> dict:

        return {

            "name":
                identity.name,

            "identity_type":
                identity.identity_type,

            "email":
                identity.email,

            "department":
                identity.department,

            "status":
                identity.status,

            "groups":
                identity.groups,

            "roles":
                identity.roles,

            "direct_permissions":
                identity.direct_permissions,

            "effective_permissions":
                identity.effective_permissions,

            "accessible_assets":
                identity.accessible_assets,
        }


    def create_delta_event(

        self,

        db: Session,

        identity_id: str,

        change_type: str,

        changed_fields: list[str],

        previous_state: dict | None,

        current_state: dict | None,

    ):

        event = IdentityDeltaEventDB(

            identity_id=identity_id,

            change_type=change_type,

            changed_fields=json.dumps(
                changed_fields
            ),

            previous_state=(
                json.dumps(
                    previous_state
                )
                if previous_state
                is not None
                else None
            ),

            current_state=(
                json.dumps(
                    current_state
                )
                if current_state
                is not None
                else None
            ),
        )


        db.add(event)


    def synchronize(

        self,

        db: Session,

    ) -> IdentitySyncResult:


        current_identities = (
            self.collect_identity_state()
        )


        stored_identities = (
            db.query(IdentityDB)
            .all()
        )


        current_by_id = {

            identity.identity_id:
                identity

            for identity
            in current_identities
        }


        stored_by_id = {

            identity.identity_id:
                identity

            for identity
            in stored_identities
        }


        created = []

        modified = []

        deleted = []

        unchanged = []


        # -------------------------
        # CREATED / MODIFIED
        # -------------------------

        for (
            identity_id,
            current
        ) in current_by_id.items():


            stored = stored_by_id.get(
                identity_id
            )


            current_state = (
                self.serialize_identity(
                    current
                )
            )


            if stored is None:


                new_identity = IdentityDB(

                    identity_id=identity_id,

                    **current_state,
                )


                db.add(
                    new_identity
                )


                self.create_delta_event(

                    db=db,

                    identity_id=identity_id,

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
                    identity_id
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

                    identity_id=identity_id,

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
                    identity_id
                )


            else:


                unchanged.append(
                    identity_id
                )


        # -------------------------
        # DELETED
        # -------------------------

        for (
            identity_id,
            stored
        ) in stored_by_id.items():


            if (
                identity_id
                not in current_by_id

                and stored.status
                != "deleted"
            ):


                previous_state = (
                    self.database_state(
                        stored
                    )
                )


                stored.status = (
                    "deleted"
                )


                current_state = (
                    self.database_state(
                        stored
                    )
                )


                self.create_delta_event(

                    db=db,

                    identity_id=identity_id,

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
                    identity_id
                )


        db.commit()


        return IdentitySyncResult(

            total_identities=len(
                current_identities
            ),

            created=created,

            modified=modified,

            deleted=deleted,

            unchanged=unchanged,
        )


identity_synchronization_service = (
    IdentitySynchronizationService()
)