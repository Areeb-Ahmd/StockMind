from pydantic import BaseModel
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict, Optional, Literal

class RagToolSchema(BaseModel):
    question:str 

class QuestionRequest(BaseModel):
    question: str

class IngestionTaskResponse(BaseModel):
    task_id: str
    status: Literal["processing", "completed", "failed"]
    current_batch: int = 0
    total_batches: int = 0
    message: str = ""
    error: Optional[str] = None