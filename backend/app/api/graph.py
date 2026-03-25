from fastapi import APIRouter
from backend.app.services.graph_builder import build_graph

router = APIRouter()

@router.get("/graph")
def get_graph():
    return build_graph()