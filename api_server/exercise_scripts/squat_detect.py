import mediapipe as mp
import cv2
import numpy as np
import sys # Import sys module

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

IMPORTANT_LMS = ["LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_HIP", "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE", "LEFT_ANKLE", "RIGHT_ANKLE"]

def extract_keypoints(results):
    landmarks = results.pose_landmarks.landmark
    return np.array([[landmarks[mp_pose.PoseLandmark[lm].value].x,
                      landmarks[mp_pose.PoseLandmark[lm].value].y,
                      landmarks[mp_pose.PoseLandmark[lm].value].z,
                      landmarks[mp_pose.PoseLandmark[lm].value].visibility] for lm in IMPORTANT_LMS]).flatten()

def rescale_frame(frame, percent=50):
    dim = (int(frame.shape[1] * percent/100), int(frame.shape[0] * percent/100))
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

def calculate_distance(p1, p2):
    return np.linalg.norm(np.array(p2) - np.array(p1))

def analyze_placement(results, thresholds, visibility_threshold):
    landmarks = results.pose_landmarks.landmark
    vis = lambda lm: landmarks[mp_pose.PoseLandmark[lm].value].visibility
    if any(vis(lm) < visibility_threshold for lm in ["LEFT_KNEE", "RIGHT_KNEE", "LEFT_ANKLE", "RIGHT_ANKLE"]):
        return {"foot": -1, "knee": -1}

    dist = lambda lm1, lm2: calculate_distance(
        [landmarks[mp_pose.PoseLandmark[lm1].value].x, landmarks[mp_pose.PoseLandmark[lm1].value].y],
        [landmarks[mp_pose.PoseLandmark[lm2].value].x, landmarks[mp_pose.PoseLandmark[lm2].value].y]
    )
    foot_shoulder_ratio = dist("LEFT_ANKLE", "RIGHT_ANKLE") / dist("LEFT_SHOULDER", "RIGHT_SHOULDER")
    return {"foot": 0 if thresholds[0] <= foot_shoulder_ratio <= thresholds[1] else (1 if foot_shoulder_ratio < thresholds[0] else 2)}

# Get video file path from command line arguments
if len(sys.argv) > 1:
    video_path = sys.argv[1]
else:
    print("Error: Video file path not provided.")
    sys.exit(1)

# Use video file instead of webcam
cap = cv2.VideoCapture(video_path)  # <- Modified here

VISIBILITY_THRESHOLD = 0.6
THRESHOLDS = [1.0, 2.8]

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    results_list = [] #Store results for aggregated printing
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        # Optionally keep/rescale frames for performance
        frame = rescale_frame(frame, 50)  # Adjust or remove this line
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        if not results.pose_landmarks: continue

        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # Comment out image display code for server execution
        # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS) # Comment out image display code for server execution

        placement = analyze_placement(results, THRESHOLDS, VISIBILITY_THRESHOLD)["foot"]
        status = "Correct" if placement == 0 else "Too tight" if placement == 1 else "Too wide" if placement == 2 else "Unknown"

        # cv2.rectangle(image, (0, 0), (300, 40), (245, 117, 16), -1) # Comment out image display code for server execution
        # cv2.putText(image, f"Foot Placement: {status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2) # Comment out image display code for server execution

        # cv2.imshow("Posture Analysis", image) # Comment out image display code for server execution

        results_list.append(status)

    cap.release()
    # cv2.destroyAllWindows() # Comment out image display code for server execution
    print(f"Squat Analysis Results: {results_list}") # Printing the results that server will retrieve from the script