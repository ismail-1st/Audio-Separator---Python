import os
import time
import shutil
from storage.storj import delete_file

TEMP_DIR = "temp"

def cleanup_job(job_id: str):
    # wait 1 hour (3600 seconds)
    time.sleep(3600)

    # local cleanup
    local_dir = os.path.join(TEMP_DIR, job_id)
    if os.path.exists(local_dir):
        shutil.rmtree(local_dir, ignore_errors=True)

    # storj cleanup
    vocals_key = f"{job_id}/vocals.wav"
    instrumentals_key = f"{job_id}/instrumentals.wav"

    try:
        delete_file(vocals_key)
        delete_file(instrumentals_key)
        print(f"[cleanup] deleted Storj files for job {job_id}")
    except Exception as e:
        print(f"[cleanup] Storj delete failed: {e}")
