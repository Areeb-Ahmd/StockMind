from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from starlette.responses import JSONResponse
from langchain_core.messages import HumanMessage
from data_ingestion.ingestion_pipeline import DataIngestion
from agent.workflow import GraphBuilder
from data_models.models import *
from utils.response_formatter import extract_text_content

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

@app.post("/query")
async def query_chatbot(request: QuestionRequest):
    try:
        graph_service = GraphBuilder()
        graph_service.build()
        graph = graph_service.get_graph()
        
        result = graph.invoke({"messages": [HumanMessage(content=request.question)]})
        
        # If result is dict with messages:
        if isinstance(result, dict) and "messages" in result and result["messages"]:
            raw_content = result["messages"][-1].content
            final_output = extract_text_content(raw_content)
        else:
            final_output = str(result)
        
        return {"answer": final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})