from fastapi import FastAPI
from app.tasks import generate_and_process_numbers
from celery.result import AsyncResult
from app.celery_worker import celery

app = FastAPI()

@app.post("/submit/")
async def submit_tasks(count: int):
    task = generate_and_process_numbers.delay(count)
    return {
        "message": f"Task submitted to generate {count} random numbers",
        "task_id": task.id
    }

@app.get("/result/{task_id}")
async def get_task_result(task_id: str):
    result = AsyncResult(task_id, app=celery)
    if result.state == "PENDING":
        return {"task_id": task_id, "status": result.state, "result": None}
    if result.state == "PROGRESS":
        return {"task_id": task_id, "status": result.state, "progress": result.info}  # this contains meta={'current': i, 'total': count}
    elif result.state == "SUCCESS":
        return {"task_id": task_id, "status": result.state, "result": result.result}
    elif result.state == "FAILURE":
        return {"task_id": task_id, "status": result.state, "error": str(result.result)}
    else:
        return {"task_id": task_id, "status": result.state}

