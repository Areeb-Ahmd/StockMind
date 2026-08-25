import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.workflow import GraphBuilder
from routers.ingestion_router import router as ingestion_router
from routers.chat_router import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Compile and cache agent state graph once on server startup
    graph_service = GraphBuilder()
    graph_service.build()
    app.state.graph = graph_service.get_graph()
    yield
    app.state.graph = None

app = FastAPI(title="StockMind API", version="0.0.1", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register modular API routers
app.include_router(ingestion_router)
app.include_router(chat_router)

@app.get("/")
async def root():
    return {"service": "StockMind API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)