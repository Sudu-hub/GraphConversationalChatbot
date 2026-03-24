from fastapi import APIRouter
from backend.app.services.graph_builder import build_graph

router = APIRouter()

@router.get("/graph")
def get_graph():
    G = build_graph()

    nodes = []
    edges = []

    # Nodes
    for node_id, data in G.nodes(data=True):
        nodes.append({
            "id": node_id,
            "label": node_id,
            "type": data.get("type", "Unknown")
        })

    # Edges
    for source, target, data in G.edges(data=True):
        edges.append({
            "source": source,
            "target": target,
            "label": data.get("label", "")
        })

    return {
        "nodes": nodes,
        "edges": edges
    }