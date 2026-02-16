from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.processor import process_url
from app.cleanup import cleanup_job
from database.firebase import database, bucket
from storage.storj import upload_file, generate_signed_url


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SeparateRequest(BaseModel):
    url: str

@app.post("/separate")
def separate(req: SeparateRequest, background_tasks: BackgroundTasks):
    # Process URL
    result = process_url(req.url)

    # Log job start in Firebase Realtime Database
    job_ref = database.reference(f"/jobs/{result['job_id']}")
    job_ref.set({"status": "started", "url": req.url})

    vocals_key = f"{result['job_id']}/vocals.wav"
    instrumentals_key = f"{result['job_id']}/instrumentals.wav"

    upload_file(result["vocals_path"], vocals_key)
    upload_file(result["instrumentals_path"], instrumentals_key)

    # Option A: public URLs
    vocals_url = f"{vocals_key}"
    instrumentals_url = f"{instrumentals_key}"

    # Option B (recommended): signed URLs
    vocals_url = generate_signed_url(vocals_key)
    instrumentals_url = generate_signed_url(instrumentals_key)

    # Schedule cleanup job
    background_tasks.add_task(cleanup_job, result["job_id"])

    # Return URLs to the frontend
    return {
        "vocals_url": vocals_url,
        "instrumentals_url": instrumentals_url,
        "job_id": result["job_id"]
    }
