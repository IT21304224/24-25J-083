import mediapipe as mp
import cv2
import numpy as np
import pandas as pd
import pickle
import sys  # Import sys module
import os
# Initialize mediapipe helpers
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Define important landmarks and headers
IMPORTANT_LMS = ["LEFT_HIP", "RIGHT_HIP"]
HEADERS = ["label"] + [f"{lm.lower()}_y" for lm in IMPORTANT_LMS]

def extract_keypoints(results):
    """Extract Y-coordinates of important landmarks."""
    return [
        results.pose_landmarks.landmark[mp_pose.PoseLandmark[lm].value].y
        for lm in IMPORTANT_LMS
    ]

def rescale_frame(frame, scale=50):
    """Rescale frame to the given percentage."""
    new_size = tuple(int(dim * scale / 100) for dim in frame.shape[1::-1])
    return cv2.resize(frame, new_size, interpolation=cv2.INTER_AREA)

def get_class_label(prediction):
    """Transform numeric prediction into class label."""
    return {0: "C", 1: "H", 2: "L"}.get(prediction, "unk")

# Load model and scaler

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the model files
model_path = os.path.join(script_dir, "train", "model", "RF_model.pkl")
scaler_path = os.path.join(script_dir, "train", "model", "input_scaler.pkl")

if not os.path.exists(model_path):
    print(f"Error: Model file not found at {model_path}", file=sys.stderr)
    sys.exit(1)

if not os.path.exists(scaler_path):
    print(f"Error: Scaler file not found at {scaler_path}", file=sys.stderr)
    sys.exit(1)


with open(model_path, "rb") as f:
    model = pickle.load(f)
with open(scaler_path, "rb") as f:
    scaler = pickle.load(f)

# Get video file path from command line arguments
if len(sys.argv) > 1:
    video_path = sys.argv[1]
else:
    print("Error: Video file path not provided.", file=sys.stderr)
    sys.exit(1)

# Use video file instead of webcam
cap = cv2.VideoCapture(video_path)

current_stage = ""
prediction_probability_threshold = 0.1

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    results_list = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Preprocess frame
        frame = rescale_frame(frame, 50)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            # Extract keypoints and make predictions
            keypoints = extract_keypoints(results)
            X = pd.DataFrame([keypoints], columns=HEADERS[1:])
            X_scaled = scaler.transform(X)
            predicted_class_numeric = model.predict(X_scaled)[0]
            probability = model.predict_proba(X_scaled)[0]

            # Convert numeric prediction to class label
            predicted_class = get_class_label(predicted_class_numeric)

            # Evaluate prediction and classify
            if probability.max() >= prediction_probability_threshold:
                current_stage = {
                    "C": "Correct",
                    "L": "Low back",
                    "H": "High back"
                }.get(predicted_class, "unk")
            else:
                current_stage = "unk"

            results_list.append(current_stage)

            # Display results (COMMENTED OUT FOR SERVER EXECUTION)
            #cv2.rectangle(frame, (0, 0), (250, 60), (245, 117, 16), -1)
            #cv2.putText(frame, "CLASS", (95, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            #cv2.putText(frame, current_stage, (90, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            #cv2.putText(frame, "PROB", (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            #cv2.putText(frame, f"{probability.max():.2f}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Draw pose landmarks (COMMENTED OUT FOR SERVER EXECUTION)
            #mp_drawing.draw_landmarks(
            #    frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            #    mp_drawing.DrawingSpec(color=(244, 117, 66), thickness=2, circle_radius=2),
            #    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=1)
            #)
        else:
            print("No human detected.", file=sys.stderr)

        #cv2.imshow("Pose Detection", frame)  # COMMENTED OUT FOR SERVER EXECUTION

    cap.release()
    #cv2.destroyAllWindows() # COMMENTED OUT FOR SERVER EXECUTION
    print(f"Plank Analysis Results: {results_list}") # Printing the results that server will retrieve from the script