from fastapi import APIRouter
from app.services.graph_builder import build_graph

router = APIRouter()

@router.post("/query")
def query_graph(data: dict):
    query = data.get("query")

    G = build_graph()

    # SIMPLE LOGIC (can upgrade later)
    if "order" in query.lower():
        return {"answer": "Orders exist in the system. Try specifying ID."}

    return {"answer": "Query understood but not implemented yet."}