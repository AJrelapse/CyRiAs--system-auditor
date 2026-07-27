from fastapi import APIRouter

from app.modules.knowledge_graph.service import (
    knowledge_graph_service,
)

router = APIRouter(
    prefix="/knowledge-graph",
    tags=["Knowledge Graph"],
)


@router.post("/build")
def build_knowledge_graph():

    return knowledge_graph_service.build()