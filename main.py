from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from starlette.responses import JSONResponse
from data_ingestion.ingestion_pipeline import DataIngestion
from agent.workflow import GraphBuilder
from data_models.models import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def uploaded_files(files: List[UploadFile] = File(...)):
    try:
        ingestion = DataIngestion()
        ingestion.run_pipeline(files)
        return {"message": "File successfully processed and stored."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})