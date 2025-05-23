from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import subprocess  # For executing Python scripts
import os

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running!"}

# Dictionary to map exercise to script path
EXERCISE_SCRIPTS = {
    "Bicep Curl": "exercise_scripts/bicep_detect.py",  # Correct script names
    "Basic Plank": "exercise_scripts/plank_detect.py",
    "Basic Squat": "exercise_scripts/squat_detect.py",
    #"Lunge": "exercise_scripts/lunge_detect.py" 
}

# Function to execute the Python script and capture output
async def execute_script(script_path, video_file_path):
    try:
        # Construct the command to execute.  Assumes Python is in the PATH.
        # Pass the video file path as an argument to the script.
        command = ["python", script_path, video_file_path]

        # Execute the script using subprocess.run (safer than os.system)
        process = subprocess.run(command, capture_output=True, text=True, timeout=60) # Adjust timeout

        # Check for errors
        if process.returncode != 0:
            error_message = process.stderr
            raise Exception(f"Script execution failed with error: {error_message}")

        # Parse the output from the script (assuming it prints JSON or a string)
        output = process.stdout
        # Potentially parse output into JSON if the scripts are modified to output JSON
        # try:
        #     results = json.loads(output)
        # except json.JSONDecodeError:
        #     results = {"output": output}  # If not JSON, return as plain text
        results = {"output": output} # Return the script output

        return results

    except subprocess.TimeoutExpired:
        raise Exception("Script execution timed out.")  # Handle timeouts
    except Exception as e:
        raise Exception(f"Error executing script: {str(e)}")


@app.post("/analyze")
async def analyze_exercise(exercise: str, video: UploadFile = File(...)):
    """
    Analyzes an exercise video using the specified Python script.
    """
    if exercise not in EXERCISE_SCRIPTS:
        return JSONResponse(content={"error": "Invalid exercise specified."}, status_code=400)

    script_path = EXERCISE_SCRIPTS[exercise]

    # Save the uploaded video to a temporary file
    video_file_path = f"temp_{video.filename}"  # Temporary filename
    try:
        contents = await video.read()
        with open(video_file_path, "wb") as f:
            f.write(contents)

        # Execute the appropriate script
        results = await execute_script(script_path, video_file_path)  # Pass file path

        return JSONResponse(content=results)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)  # Server error

    finally:
        # Clean up the temporary video file
        if os.path.exists(video_file_path):
            os.remove(video_file_path)  # Remove after processing