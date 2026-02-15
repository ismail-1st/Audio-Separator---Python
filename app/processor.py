import os
import subprocess
import uuid
import sys

TEMP_DIR = "temp"

os.makedirs(TEMP_DIR, exist_ok=True)

def process_url(url: str):
    job_id = str(uuid.uuid4())
    input_path = f"{TEMP_DIR}/{job_id}.mp3"
    output_dir = f"{TEMP_DIR}/{job_id}_out"

    subprocess.run([
        sys.executable, "-m", "yt_dlp",
        "-x",
        "--audio-format", "mp3",
        "-o", input_path,
        url
    ], check=True)

    subprocess.run([
        sys.executable, "-m", "demucs",
        "--two-stems=vocals",
        "-n", "mdx_extra_q",
        input_path,
        "-o",
        output_dir
    ], check=True)

    base = f"{output_dir}/mdx_extra_q/{job_id}"

    vocals_path = f"{base}/vocals.wav"
    instrumentals_path = f"{base}/no_vocals.wav"

    return {
        "job_id": job_id,
        "vocals_path": vocals_path,
        "instrumentals_path": instrumentals_path
    }
