from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.services.query_engine import process_query

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
def query(req: QueryRequest):
    return process_query(req.question)