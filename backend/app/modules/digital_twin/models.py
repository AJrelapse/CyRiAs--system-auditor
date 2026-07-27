from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class TwinNode(BaseModel):
    node_id: str
    node_type: str
    label: str
    properties: dict[str, Any] = Field(
        default_factory=dict
    )


class TwinEdge(BaseModel):
    source: str
    target: str
    relationship: str
    properties: dict[str, Any] = Field(
        default_factory=dict
    )


class DigitalTwinGraph(BaseModel):
    generated_at: datetime
    node_count: int
    edge_count: int

    nodes: list[TwinNode]
    edges: list[TwinEdge]


class DigitalTwinBuildResult(BaseModel):
    status: str
    node_count: int
    edge_count: int
    generated_at: datetime

class TwinSyncResult(BaseModel):
    status: str

    processed_changes: int

    affected_nodes: list[str] = Field(
        default_factory=list
    )

    sources_processed: list[str] = Field(
        default_factory=list
    )

    node_count: int

    edge_count: int

    synchronized_at: datetime


class TwinChangeResponse(BaseModel):
    change_id: str
    entity_id: str
    entity_type: str
    change_type: str
    source_module: str
    details: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }