import io
import uuid
from typing import List, Dict, Any, Optional
from fastapi import BackgroundTasks
from data_ingestion.ingestion_pipeline import DataIngestion
from data_models.models import IngestionTaskResponse

class BufferedUploadFile:
    """In-memory wrapper for UploadFile bytes so background tasks can safely read contents."""
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.file = io.BytesIO(content)

class TaskService:
    """Service to handle background ingestion tasks and track progress state."""

    def __init__(self):
        self._ingestion_tasks: Dict[str, Dict[str, Any]] = {}

    def _update_progress(self, task_id: str, current_batch: int, total_batches: int, message: str):
        if task_id in self._ingestion_tasks:
            self._ingestion_tasks[task_id]["current_batch"] = current_batch
            self._ingestion_tasks[task_id]["total_batches"] = total_batches
            self._ingestion_tasks[task_id]["message"] = message

    def process_ingestion_task(self, task_id: str, files: List[BufferedUploadFile]):
        try:
            self._ingestion_tasks[task_id]["status"] = "processing"
            self._ingestion_tasks[task_id]["message"] = "Starting ingestion pipeline..."

            ingestion = DataIngestion()
            ingestion.run_pipeline(
                files,
                progress_callback=lambda curr, tot, msg: self._update_progress(task_id, curr, tot, msg)
            )

            self._ingestion_tasks[task_id]["status"] = "completed"
            self._ingestion_tasks[task_id]["message"] = "Successfully processed and stored all document chunks."
        except Exception as e:
            self._ingestion_tasks[task_id]["status"] = "failed"
            self._ingestion_tasks[task_id]["error"] = str(e)
            self._ingestion_tasks[task_id]["message"] = f"Ingestion failed: {str(e)}"

    def create_task(self, files: List[BufferedUploadFile], background_tasks: BackgroundTasks) -> IngestionTaskResponse:
        task_id = str(uuid.uuid4())
        self._ingestion_tasks[task_id] = {
            "task_id": task_id,
            "status": "processing",
            "current_batch": 0,
            "total_batches": 0,
            "message": "Upload received, starting ingestion background task...",
            "error": None
        }

        background_tasks.add_task(self.process_ingestion_task, task_id, files)
        return IngestionTaskResponse(**self._ingestion_tasks[task_id])

    def get_task_status(self, task_id: str) -> Optional[IngestionTaskResponse]:
        if task_id not in self._ingestion_tasks:
            return None
        return IngestionTaskResponse(**self._ingestion_tasks[task_id])

# Singleton service instance
task_service = TaskService()
