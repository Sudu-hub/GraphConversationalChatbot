from fastapi import FastAPI
from backend.app.api.graph import router as graph_router

app = FastAPI()

app.include_router(graph_router)