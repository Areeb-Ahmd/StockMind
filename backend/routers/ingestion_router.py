from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from typing import List
from starlette.responses import JSONResponse
from data_models.models import IngestionTaskResponse
from services.task_service import task_service, BufferedUploadFile

router = APIRouter(tags=["Document Ingestion"])

@router.post("/upload", status_code=202, response_model=IngestionTaskResponse)
async def upload_files(background_tasks: BackgroundTasks, files: List[UploadFile] = File(...)):
    try:
        buffered_files = []
        for f in files:
            content = await f.read()
            buffered_files.append(BufferedUploadFile(filename=f.filename, content=content))

        return task_service.create_task(buffered_files, background_tasks)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/upload/status/{task_id}")
async def get_upload_status(task_id: str):
    task_response = task_service.get_task_status(task_id)
    if task_response is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    return task_response
