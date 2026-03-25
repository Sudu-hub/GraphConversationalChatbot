from fastapi import FastAPI
from backend.app.utils.mapper import load_all_data
from backend.app.api.graph import router as graph_router

app = FastAPI()

data_store = load_all_data()
app.include_router(graph_router)

@app.get("/")
def home():
    return {"message": "O2C Graph Backend Running 🚀"}

@app.get("/tables")
def get_tables():
    return list(data_store.keys())

@app.get("/preview/{table}")
def preview(table: str):
    if table not in data_store:
        return {"error": "Table not found"}
    
    return data_store[table].head(5).to_dict(orient="records")