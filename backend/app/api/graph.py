from fastapi import APIRouter
from backend.app.services.graph_builder import build_graph

router = APIRouter()

GRAPH_DATA = {"nodes": [], "links": []}


GRAPH_DATA = build_graph()

@router.get("/graph")
def get_graph():
    global GRAPH_DATA
    GRAPH_DATA = build_graph()
    return GRAPH_DATA