import shutil
import os

def cleanup_job(job_id: str):
    base = "temp"
    paths = [
        f"{base}/{job_id}.mp3",
        f"{base}/{job_id}_out",
        f"{base}/{job_id}.zip",
    ]

    for path in paths:
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
        elif os.path.isfile(path):
            try:
                os.remove(path)
            except Exception:
                pass
