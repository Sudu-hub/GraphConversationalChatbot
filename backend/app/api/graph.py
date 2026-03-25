from fastapi import APIRouter
from backend.app.services.graph_builder import build_graph

router = APIRouter()

GRAPH_DATA = {"nodes": [], "links": []}


@router.get("/graph")
def get_graph():
    global GRAPH_DATA

    # 🔥 your existing graph builder
    GRAPH_DATA = build_graph()   # <-- your function

    return GRAPH_DATA