from fastapi import FastAPI
from pydantic import BaseModel
from app.processor import process_url
from fastapi.responses import FileResponse
import zipfile

app = FastAPI()

class SeparateRequest(BaseModel):
    url:str

@app.post("/separate")
def separate(req: SeparateRequest):
    result = process_url(req.url)

    zip_path = f"temp/{result['job_id']}.zip"

    with zipfile.ZipFile(zip_path, 'w') as z:
        z.write(result["vocals_path"], arcname="vocals.wav")
        z.write(result["instrumentals_path"], arcname="instrumentals.wav")

    return FileResponse(zip_path, media_type="application/zip", filename="stems.zip")
