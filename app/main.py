from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from app.processor import process_url
from app.cleanup import cleanup_job
from fastapi.responses import FileResponse
import zipfile

app = FastAPI()

class SeparateRequest(BaseModel):
    url:str

@app.post("/separate")
def separate(req: SeparateRequest, background_tasks: BackgroundTasks):
    result = process_url(req.url)

    zip_path = f"temp/{result['job_id']}.zip"

    with zipfile.ZipFile(zip_path, 'w') as z:
        z.write(result["vocals_path"], arcname="vocals.wav")
        z.write(result["instrumentals_path"], arcname="instrumentals.wav")

    background_tasks.add_task(cleanup_job, result["job_id"])

    return FileResponse(zip_path, media_type="application/zip", filename="stems.zip")
