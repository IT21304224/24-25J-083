from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import subprocess
import os

app = FastAPI()

# Dictionary to map exercise to script path
EXERCISE_SCRIPTS = {
    "Bicep Curl": "exercise_scripts/bicep_detect.py",
    "Basic Plank": "exercise_scripts/plank_detect.py",
    "Basic Squat": "exercise_scripts/squat_detect.py",
}

async def execute_script(script_path, video_file_path):
    """Run the specified script and capture the output."""
    try:
        command = ["python", script_path, video_file_path]
        process = subprocess.run(command, capture_output=True, text=True, timeout=60)

        if process.returncode != 0:
            return {"error": process.stderr}

        return {"output": process.stdout}

    except subprocess.TimeoutExpired:
        return {"error": "Script execution timed out."}
    except Exception as e:
        return {"error": str(e)}

@app.post("/analyze")
async def analyze_exercise(
    exercise: str = Form(...),  # Accepts exercise name from form-data
    video: UploadFile = File(...)  # Accepts video file
):
    """Analyzes an exercise video."""
    if exercise not in EXERCISE_SCRIPTS:
        return JSONResponse(content={"error": "Invalid exercise specified."}, status_code=400)

    script_path = EXERCISE_SCRIPTS[exercise]
    video_file_path = f"temp_{video.filename}"

    try:
        contents = await video.read()
        with open(video_file_path, "wb") as f:
            f.write(contents)

        # Execute the script
        results = await execute_script(script_path, video_file_path)

        return JSONResponse(content=results)

    finally:
        if os.path.exists(video_file_path):
            os.remove(video_file_path)  # Cleanup
