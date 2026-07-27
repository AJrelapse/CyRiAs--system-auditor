import json
from datetime import datetime, timezone

import networkx as nx

from sqlalchemy.orm import Session

from app.db.models import (
    AssetDB,
    AssetConfigurationDB,
    AssetChangeEventDB,
    CloudResourceDB,
    CloudDeltaEventDB,
    IdentityDB,
    IdentityDeltaEventDB,
    SecurityEventDB,
    DigitalTwinSnapshotDB,
    DigitalTwinChangeDB,
    TwinProcessedEventDB,
    ConfigurationDeltaEventDB,
)

from .models import (
    TwinNode,
    TwinEdge,
    DigitalTwinGraph,
    DigitalTwinBuildResult,
    TwinSyncResult,
)

class DigitalTwinService:

    def __init__(self):

        self.graph = nx.MultiDiGraph()

    def is_event_processed(
        self,
        db: Session,
        event_id: str,
        source_module: str,
    ) -> bool:

        return (
            db.query(TwinProcessedEventDB)
            .filter(
                TwinProcessedEventDB.source_event_id == event_id,
                TwinProcessedEventDB.source_module == source_module,
            )
            .first()
            is not None
        )
    
    def process_behavioral_events(
        self,
        db: Session,
        affected_nodes: set[str],
    ) -> int:

        events = (

            db.query(
                SecurityEventDB
            )

            .order_by(
                SecurityEventDB.timestamp
            )

            .all()
        )


        processed = 0

        affected_assets = set()


        for event in events:

            if self.is_event_processed(
                db,
                event.event_id,
                "log_collection",
            ):

                continue


            # Events without an asset cannot
            # update an asset node.

            if event.asset_id:

                affected_assets.add(
                    event.asset_id
                )


                affected_nodes.add(
                    event.asset_id
                )


                self.record_twin_change(

                    db=db,

                    entity_id=event.asset_id,

                    entity_type="behavior",

                    change_type=(
                        "SECURITY_EVENT"
                    ),

                    source_module=(
                        "log_collection"
                    ),

                    details={

                        "source_event_id":
                            event.event_id,

                        "severity":
                            event.severity,

                        "category":
                            event.category,
                    },
                )


            self.mark_event_processed(

                db,

                event.event_id,

                "log_collection",
            )


            processed += 1


        # Refresh each affected asset only once,
        # even if it received many new events.

        for asset_id in affected_assets:

            self.refresh_asset_behavior(

                db,

                asset_id,
            )


        return processed
    
    def refresh_asset_behavior(
        self,
        db: Session,
        asset_id: str,
    ):

        if not self.graph.has_node(
            asset_id
        ):

            return


        events = (

            db.query(
                SecurityEventDB
            )

            .filter(
                SecurityEventDB.asset_id
                == asset_id
            )

            .all()
        )


        state = {

            "total_events": 0,

            "critical_events": 0,

            "high_events": 0,

            "failed_authentications": 0,

            "malware_events": 0,
        }


        for event in events:

            state[
                "total_events"
            ] += 1


            if event.severity == "critical":

                state[
                    "critical_events"
                ] += 1


            if event.severity == "high":

                state[
                    "high_events"
                ] += 1


            if (
                event.category
                == "authentication"

                and event.successful
                is False
            ):

                state[
                    "failed_authentications"
                ] += 1


            if event.category == "malware":

                state[
                    "malware_events"
                ] += 1


        self.graph.nodes[
            asset_id
        ][
            "behavioral_state"
        ] = state
    
    def process_configuration_events(
        self,
        db: Session,
        affected_nodes: set[str],
    ) -> int:

        events = (

            db.query(
                ConfigurationDeltaEventDB
            )

            .order_by(
                ConfigurationDeltaEventDB
                .created_at
            )

            .all()
        )


        processed = 0


        for event in events:

            if self.is_event_processed(
                db,
                event.event_id,
                "configuration_collection",
            ):

                continue


            self.refresh_asset_configuration(

                db,

                event.asset_id,
            )


            self.refresh_configuration_relationships(

                db,

                event.asset_id,
            )


            affected_nodes.add(
                event.asset_id
            )


            self.record_twin_change(

                db=db,

                entity_id=event.asset_id,

                entity_type=(
                    "configuration"
                ),

                change_type=(
                    event.change_type
                ),

                source_module=(
                    "configuration_collection"
                ),

                details={

                    "source_event_id":
                        event.event_id,

                    "changed_fields":
                        event.changed_fields,
                },
            )


            self.mark_event_processed(

                db,

                event.event_id,

                "configuration_collection",
            )


            processed += 1


        return processed

    def refresh_configuration_relationships(
        self,
        db: Session,
        asset_id: str,
    ):

        if not self.graph.has_node(
            asset_id
        ):
            return


        # Remove configuration-derived incoming
        # network relationships for this asset.

        incoming_edges = list(

            self.graph.in_edges(
                asset_id,
                keys=True,
                data=True,
            )
        )


        for (
            source,
            target,
            key,
            attributes
        ) in incoming_edges:

            if attributes.get(
                "relationship"
            ) in {
                "NETWORK_ACCESS",
                "CONNECTS_TO",
            }:

                self.graph.remove_edge(
                    source,
                    target,
                    key,
                )


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
            return


        firewall_rules = json.loads(
            configuration.firewall_rules
        )


        for rule in firewall_rules:

            if rule.get(
                "action"
            ) != "ALLOW":

                continue


            source = rule.get(
                "source"
            )

            port = rule.get(
                "destination_port"
            )

            protocol = rule.get(
                "protocol"
            )


            if source == "0.0.0.0/0":

                if not self.graph.has_node(
                    "INTERNET"
                ):

                    self.graph.add_node(

                        "INTERNET",

                        node_type="external",

                        label="Internet",
                    )


                self.graph.add_edge(

                    "INTERNET",

                    asset_id,

                    relationship=(
                        "NETWORK_ACCESS"
                    ),

                    port=port,

                    protocol=protocol,

                    source_module=(
                        "configuration"
                    ),
                )


            elif self.graph.has_node(
                source
            ):

                self.graph.add_edge(

                    source,

                    asset_id,

                    relationship=(
                        "CONNECTS_TO"
                    ),

                    port=port,

                    protocol=protocol,

                    source_module=(
                        "configuration"
                    ),
                )

    def mark_event_processed(
        self,
        db: Session,
        event_id: str,
        source_module: str,
    ):

        db.add(
            TwinProcessedEventDB(
                source_event_id=event_id,
                source_module=source_module,
            )
        )


    def record_twin_change(
        self,
        db: Session,
        entity_id: str,
        entity_type: str,
        change_type: str,
        source_module: str,
        details: dict,
    ):

        db.add(
            DigitalTwinChangeDB(
                entity_id=entity_id,
                entity_type=entity_type,
                change_type=change_type,
                source_module=source_module,
                details=json.dumps(details),
            )
        )

    def refresh_asset_node(
        self,
        db: Session,
        asset_id: str,
    ):

        asset = (
            db.query(AssetDB)
            .filter(
                AssetDB.asset_id == asset_id
            )
            .first()
        )

        if (
            asset is None
            or asset.status == "removed"
        ):
            if self.graph.has_node(asset_id):
                self.graph.remove_node(asset_id)

            return

        existing_attributes = {}

        if self.graph.has_node(asset_id):
            existing_attributes = dict(
                self.graph.nodes[asset_id]
            )

        updated_attributes = {
            **existing_attributes,
            "node_type": "asset",
            "label": asset.name,
            "asset_type": asset.asset_type,
            "criticality": asset.criticality,
            "environment": asset.environment,
            "provider": asset.provider,
            "region": asset.region,
            "ip_address": asset.ip_address,
            "operating_system": asset.operating_system,
        }

        self.graph.add_node(
            asset_id,
            **updated_attributes,
        )

    def refresh_asset_configuration(
        self,
        db: Session,
        asset_id: str,
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


        if (
            configuration is None
            or not self.graph.has_node(
                asset_id
            )
        ):
            return


        node = self.graph.nodes[
            asset_id
        ]


        node["hostname"] = (
            configuration.hostname
        )

        node["patch_level"] = (
            configuration.patch_level
        )

        node["open_ports"] = json.loads(
            configuration.open_ports
        )

        node["installed_software"] = (
            json.loads(
                configuration
                .installed_software
            )
        )

        node["security_controls"] = (
            json.loads(
                configuration
                .security_controls
            )
        )

        node[
            "configuration_metadata"
        ] = json.loads(
            configuration
            .configuration_metadata
        )

    def refresh_identity_node(
        self,
        db: Session,
        identity_id: str,
    ):

        identity = (

            db.query(IdentityDB)

            .filter(
                IdentityDB.identity_id
                == identity_id
            )

            .first()
        )


        if (
            identity is None
            or identity.status == "deleted"
        ):

            if self.graph.has_node(
                identity_id
            ):
                self.graph.remove_node(
                    identity_id
                )

            return


        groups = json.loads(
            identity.groups
        )

        roles = json.loads(
            identity.roles
        )

        permissions = json.loads(
            identity.effective_permissions
        )

        accessible_assets = json.loads(
            identity.accessible_assets
        )


        # Remove old outgoing identity edges.

        if self.graph.has_node(
            identity_id
        ):

            outgoing_edges = list(
                self.graph.out_edges(
                    identity_id,
                    keys=True,
                )
            )

            for (
                source,
                target,
                key
            ) in outgoing_edges:

                self.graph.remove_edge(
                    source,
                    target,
                    key,
                )


        self.graph.add_node(

            identity_id,

            node_type="identity",

            identity_type=(
                identity.identity_type
            ),

            label=identity.name,

            department=(
                identity.department
            ),

            roles=roles,

            effective_permissions=(
                permissions
            ),
        )


        for group_id in groups:

            if self.graph.has_node(
                group_id
            ):

                self.graph.add_edge(

                    identity_id,

                    group_id,

                    relationship="MEMBER_OF",
                )


        for asset_id in accessible_assets:

            if not self.graph.has_node(
                asset_id
            ):

                continue


            relationship = "HAS_ACCESS"


            if any(

                "admin"
                in permission.lower()

                for permission
                in permissions
            ):

                relationship = (
                    "ADMIN_ACCESS"
                )


            self.graph.add_edge(

                identity_id,

                asset_id,

                relationship=relationship,
            )

    def process_asset_events(
        self,
        db: Session,
        affected_nodes: set[str],
    ) -> int:

        events = (
            db.query(AssetChangeEventDB)
            .order_by(
                AssetChangeEventDB.created_at
            )
            .all()
        )


        processed = 0


        for event in events:

            if self.is_event_processed(
                db,
                event.event_id,
                "asset_discovery",
            ):
                continue


            self.refresh_asset_node(
                db,
                event.asset_id,
            )


            self.refresh_asset_configuration(
                db,
                event.asset_id,
            )


            affected_nodes.add(
                event.asset_id
            )


            self.record_twin_change(

                db=db,

                entity_id=event.asset_id,

                entity_type="asset",

                change_type=(
                    event.change_type
                ),

                source_module=(
                    "asset_discovery"
                ),

                details={
                    "source_event_id":
                        event.event_id,

                    "changed_fields":
                        event.changed_fields,
                },
            )


            self.mark_event_processed(

                db,

                event.event_id,

                "asset_discovery",
            )


            processed += 1


        return processed
    
    def process_identity_events(
        self,
        db: Session,
        affected_nodes: set[str],
    ) -> int:

        events = (

            db.query(
                IdentityDeltaEventDB
            )

            .order_by(
                IdentityDeltaEventDB
                .created_at
            )

            .all()
        )


        processed = 0


        for event in events:

            if self.is_event_processed(
                db,
                event.event_id,
                "identity_synchronization",
            ):
                continue


            self.refresh_identity_node(

                db,

                event.identity_id,
            )


            affected_nodes.add(
                event.identity_id
            )


            self.record_twin_change(

                db=db,

                entity_id=(
                    event.identity_id
                ),

                entity_type="identity",

                change_type=(
                    event.change_type
                ),

                source_module=(
                    "identity_synchronization"
                ),

                details={

                    "source_event_id":
                        event.event_id,

                    "changed_fields":
                        event.changed_fields,
                },
            )


            self.mark_event_processed(

                db,

                event.event_id,

                "identity_synchronization",
            )


            processed += 1


        return processed

    def refresh_cloud_resource(
        self,
        db: Session,
        asset_id: str,
    ):
        if not self.graph.has_node(asset_id):
            return

        resources = (
            db.query(CloudResourceDB)
            .filter(
                CloudResourceDB.asset_id == asset_id,
                CloudResourceDB.status != "deleted",
            )
            .all()
        )

        node = self.graph.nodes[asset_id]

        node["cloud_resources"] = [
            resource.resource_id
            for resource in resources
        ]

    def process_cloud_events(
        self,
        db: Session,
        affected_nodes: set[str],
    ) -> int:

        events = (

            db.query(
                CloudDeltaEventDB
            )

            .order_by(
                CloudDeltaEventDB
                .created_at
            )

            .all()
        )


        processed = 0


        for event in events:

            if self.is_event_processed(
                db,
                event.event_id,
                "cloud_synchronization",
            ):
                continue


            resource = (

                db.query(
                    CloudResourceDB
                )

                .filter(
                    CloudResourceDB.resource_id
                    == event.resource_id
                )

                .first()
            )


            affected_id = (
                resource.asset_id
                if resource
                and resource.asset_id
                else event.resource_id
            )

            self.refresh_cloud_resource(
                db,
                affected_id,
            )

            affected_nodes.add(
                affected_id
            )


            self.record_twin_change(

                db=db,

                entity_id=affected_id,

                entity_type="cloud",

                change_type=(
                    event.change_type
                ),

                source_module=(
                    "cloud_synchronization"
                ),

                details={

                    "source_event_id":
                        event.event_id,

                    "resource_id":
                        event.resource_id,

                    "changed_fields":
                        event.changed_fields,
                },
            )


            self.mark_event_processed(

                db,

                event.event_id,

                "cloud_synchronization",
            )


            processed += 1


        return processed
    
    def synchronize_incrementally(
        self,
        db: Session,
    ) -> TwinSyncResult:

        # Ensure a baseline graph exists.

        if (
            self.graph.number_of_nodes()
            == 0
        ):

            self.build_twin(
                db
            )


        affected_nodes: set[str] = set()

        sources_processed = []

        processed_changes = 0


        asset_changes = (
            self.process_asset_events(
                db,
                affected_nodes,
            )
        )


        if asset_changes:

            sources_processed.append(
                "asset_discovery"
            )

            processed_changes += (
                asset_changes
            )

        configuration_changes = (
            self.process_configuration_events(
                db,
                affected_nodes,
            )
        )

        if configuration_changes:

            sources_processed.append(
                "configuration_collection"
            )

            processed_changes += (
                configuration_changes
            )


        identity_changes = (
            self.process_identity_events(
                db,
                affected_nodes,
            )
        )


        if identity_changes:

            sources_processed.append(
                "identity_synchronization"
            )

            processed_changes += (
                identity_changes
            )


        cloud_changes = (
            self.process_cloud_events(
                db,
                affected_nodes,
            )
        )


        if cloud_changes:

            sources_processed.append(
                "cloud_synchronization"
            )

            processed_changes += (
                cloud_changes
            )

        behavioral_changes = (
            self.process_behavioral_events(
                db,
                affected_nodes,
            )
        )

        if behavioral_changes:

            sources_processed.append(
                "log_collection"
            )

            processed_changes += (
                behavioral_changes
            )


        db.commit()


        return TwinSyncResult(

            status="synchronized",

            processed_changes=(
                processed_changes
            ),

            affected_nodes=sorted(
                affected_nodes
            ),

            sources_processed=(
                sources_processed
            ),

            node_count=(
                self.graph.number_of_nodes()
            ),

            edge_count=(
                self.graph.number_of_edges()
            ),

            synchronized_at=(
                datetime.now(
                    timezone.utc
                )
            ),
        )

    def reset_graph(self):

        self.graph.clear()

    def add_asset_nodes(
        self,
        db: Session,
    ):

        assets = (
            db.query(AssetDB)
            .filter(
                AssetDB.status != "removed"
            )
            .all()
        )


        for asset in assets:

            self.graph.add_node(

                asset.asset_id,

                node_type="asset",

                label=asset.name,

                asset_type=asset.asset_type,

                criticality=asset.criticality,

                environment=asset.environment,

                provider=asset.provider,

                region=asset.region,

                ip_address=asset.ip_address,

                operating_system=(
                    asset.operating_system
                ),
            )
    def enrich_with_configurations(
        self,
        db: Session,
    ):

        configurations = (
            db.query(
                AssetConfigurationDB
            )
            .all()
        )


        for configuration in configurations:

            if not self.graph.has_node(
                configuration.asset_id
            ):

                continue


            node = self.graph.nodes[
                configuration.asset_id
            ]


            node["hostname"] = (
                configuration.hostname
            )

            node["patch_level"] = (
                configuration.patch_level
            )

            node["open_ports"] = (
                json.loads(
                    configuration.open_ports
                )
            )

            node["installed_software"] = (
                json.loads(
                    configuration
                    .installed_software
                )
            )

            node["security_controls"] = (
                json.loads(
                    configuration
                    .security_controls
                )
            )

            node[
                "configuration_metadata"
            ] = json.loads(
                configuration
                .configuration_metadata
            )
    
    def add_configuration_relationships(
        self,
        db: Session,
    ):

        configurations = (
            db.query(
                AssetConfigurationDB
            )
            .all()
        )


        for configuration in configurations:

            firewall_rules = json.loads(
                configuration.firewall_rules
            )


            for rule in firewall_rules:

                if (
                    rule.get("action")
                    != "ALLOW"
                ):
                    continue


                source = rule.get(
                    "source"
                )


                destination = (
                    configuration.asset_id
                )


                port = rule.get(
                    "destination_port"
                )


                protocol = rule.get(
                    "protocol"
                )


                # Public internet source

                if source == "0.0.0.0/0":

                    if not self.graph.has_node(
                        "INTERNET"
                    ):

                        self.graph.add_node(

                            "INTERNET",

                            node_type=(
                                "external"
                            ),

                            label="Internet",
                        )


                    self.graph.add_edge(

                        "INTERNET",

                        destination,

                        relationship=(
                            "NETWORK_ACCESS"
                        ),

                        port=port,

                        protocol=protocol,
                    )


                # Known enterprise asset

                elif self.graph.has_node(
                    source
                ):

                    self.graph.add_edge(

                        source,

                        destination,

                        relationship=(
                            "CONNECTS_TO"
                        ),

                        port=port,

                        protocol=protocol,
                    )
    
    def add_identity_nodes(
        self,
        db: Session,
    ):

        identities = (
            db.query(IdentityDB)
            .filter(
                IdentityDB.status
                != "deleted"
            )
            .all()
        )


        for identity in identities:

            groups = json.loads(
                identity.groups
            )

            roles = json.loads(
                identity.roles
            )

            permissions = json.loads(
                identity.effective_permissions
            )

            accessible_assets = json.loads(
                identity.accessible_assets
            )


            self.graph.add_node(

                identity.identity_id,

                node_type="identity",

                identity_type=(
                    identity.identity_type
                ),

                label=identity.name,

                department=(
                    identity.department
                ),

                roles=roles,

                effective_permissions=(
                    permissions
                ),
            )


            # Group membership

            for group_id in groups:

                self.graph.add_edge(

                    identity.identity_id,

                    group_id,

                    relationship="MEMBER_OF",
                )


            # Asset access

            for asset_id in accessible_assets:

                if not self.graph.has_node(
                    asset_id
                ):

                    continue


                relationship = "HAS_ACCESS"


                if any(

                    "admin"
                    in permission.lower()

                    for permission
                    in permissions
                ):

                    relationship = (
                        "ADMIN_ACCESS"
                    )


                self.graph.add_edge(

                    identity.identity_id,

                    asset_id,

                    relationship=relationship,
                )

    def add_cloud_state(
        self,
        db: Session,
    ):

        resources = (
            db.query(
                CloudResourceDB
            )
            .filter(
                CloudResourceDB.status
                != "deleted"
            )
            .all()
        )


        for resource in resources:

            configuration = json.loads(
                resource.configuration
            )


            # Resource already represented
            # by an enterprise asset.

            if (
                resource.asset_id
                and self.graph.has_node(
                    resource.asset_id
                )
            ):

                node = self.graph.nodes[
                    resource.asset_id
                ]

                cloud_resources = node.get(
                    "cloud_resources",
                    [],
                )

                cloud_resources.append(
                    resource.resource_id
                )

                node["cloud_resources"] = (
                    cloud_resources
                )


            # IAM roles become graph nodes

            if (
                resource.resource_type
                == "iam_role"
            ):

                self.graph.add_node(

                    resource.resource_id,

                    node_type="cloud_identity",

                    label=resource.name,

                    provider=resource.provider,
                )


                principal = (
                    configuration.get(
                        "principal_asset"
                    )
                )

                target = (
                    configuration.get(
                        "target_asset"
                    )
                )

                permissions = (
                    configuration.get(
                        "permissions",
                        [],
                    )
                )


                if (
                    principal
                    and self.graph.has_node(
                        principal
                    )
                ):

                    self.graph.add_edge(

                        principal,

                        resource.resource_id,

                        relationship=(
                            "ASSUMES_ROLE"
                        ),
                    )


                if (
                    target
                    and self.graph.has_node(
                        target
                    )
                ):

                    self.graph.add_edge(

                        resource.resource_id,

                        target,

                        relationship=(
                            "GRANTS_ACCESS"
                        ),

                        permissions=permissions,
                    )
    
    def enrich_with_behavior(
        self,
        db: Session,
    ):

        events = (
            db.query(
                SecurityEventDB
            )
            .all()
        )


        behavior = {}


        for event in events:

            if not event.asset_id:

                continue


            if event.asset_id not in behavior:

                behavior[event.asset_id] = {

                    "total_events": 0,

                    "critical_events": 0,

                    "high_events": 0,

                    "failed_authentications": 0,

                    "malware_events": 0,
                }


            state = behavior[
                event.asset_id
            ]


            state[
                "total_events"
            ] += 1


            if event.severity == "critical":

                state[
                    "critical_events"
                ] += 1


            if event.severity == "high":

                state[
                    "high_events"
                ] += 1


            if (
                event.category
                == "authentication"
                and event.successful is False
            ):

                state[
                    "failed_authentications"
                ] += 1


            if event.category == "malware":

                state[
                    "malware_events"
                ] += 1


        for asset_id, state in behavior.items():

            if self.graph.has_node(
                asset_id
            ):

                self.graph.nodes[
                    asset_id
                ][
                    "behavioral_state"
                ] = state

    def export_graph(
        self,
    ) -> DigitalTwinGraph:

        nodes = []

        edges = []


        for (
            node_id,
            attributes
        ) in self.graph.nodes(
            data=True
        ):

            attributes = dict(
                attributes
            )

            node_type = (
                attributes.pop(
                    "node_type",
                    "unknown",
                )
            )

            label = attributes.pop(
                "label",
                node_id,
            )


            nodes.append(

                TwinNode(

                    node_id=str(
                        node_id
                    ),

                    node_type=(
                        node_type
                    ),

                    label=label,

                    properties=(
                        attributes
                    ),
                )
            )


        for (
            source,
            target,
            attributes
        ) in self.graph.edges(
            data=True
        ):

            attributes = dict(
                attributes
            )


            relationship = (
                attributes.pop(
                    "relationship",
                    "RELATED_TO",
                )
            )


            edges.append(

                TwinEdge(

                    source=str(
                        source
                    ),

                    target=str(
                        target
                    ),

                    relationship=(
                        relationship
                    ),

                    properties=(
                        attributes
                    ),
                )
            )


        return DigitalTwinGraph(

            generated_at=(
                datetime.now(
                    timezone.utc
                )
            ),

            node_count=(
                self.graph
                .number_of_nodes()
            ),

            edge_count=(
                self.graph
                .number_of_edges()
            ),

            nodes=nodes,

            edges=edges,
        )
    
    def build_twin(
        self,
        db: Session,
    ) -> DigitalTwinGraph:

        self.reset_graph()


        # Module 1
        self.add_asset_nodes(
            db
        )


        # Module 3
        self.enrich_with_configurations(
            db
        )

        self.add_configuration_relationships(
            db
        )


        # Module 5
        self.add_identity_nodes(
            db
        )


        # Module 4
        self.add_cloud_state(
            db
        )


        # Module 2
        self.enrich_with_behavior(
            db
        )


        twin = self.export_graph()


        snapshot = DigitalTwinSnapshotDB(

            node_count=(
                twin.node_count
            ),

            edge_count=(
                twin.edge_count
            ),

            graph_data=(
                twin.model_dump_json()
            ),
        )


        db.add(
            snapshot
        )

        db.commit()


        return twin
    
digital_twin_service = (
    DigitalTwinService()
)