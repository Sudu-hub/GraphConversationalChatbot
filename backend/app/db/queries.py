from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.services.query_engine import process_query
from backend.app.api.graph import GRAPH_DATA

router = APIRouter()

class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def query_graph(req: QueryRequest):
    return process_query(req.question, GRAPH_DATA)