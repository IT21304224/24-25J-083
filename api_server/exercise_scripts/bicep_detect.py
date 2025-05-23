import mediapipe as mp
import cv2
import numpy as np
import sys  # Import sys module

# Mediapipe helpers
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    """Calculate the angle between three points."""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return angle if angle <= 180 else 360 - angle

def detect_loose_upper_arm(landmarks, side, threshold=40):
    """Detect loose upper arm based on the angle with the vertical axis."""
    shoulder = [landmarks[mp_pose.PoseLandmark[f"{side}_SHOULDER"].value].x,
                landmarks[mp_pose.PoseLandmark[f"{side}_SHOULDER"].value].y]
    elbow = [landmarks[mp_pose.PoseLandmark[f"{side}_ELBOW"].value].x,
             landmarks[mp_pose.PoseLandmark[f"{side}_ELBOW"].value].y]

    shoulder_projection = [shoulder[0], 1]  # Projection of shoulder to vertical axis
    angle = calculate_angle(elbow, shoulder, shoulder_projection)
    return angle > threshold, angle

# Get video file path from command line arguments
if len(sys.argv) > 1:
    video_path = sys.argv[1]
else:
    print("Error: Video file path not provided.", file=sys.stderr)
    sys.exit(1)

# Use video file instead of webcam
cap = cv2.VideoCapture(video_path)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    results_list = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Preprocess frame
        frame = cv2.resize(frame, (640, 480))
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)

        # Draw landmarks
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.pose_landmarks:
            #mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS) # Comment out image display code for server execution

            # Detect loose upper arm
            landmarks = results.pose_landmarks.landmark
            loose_left, left_angle = detect_loose_upper_arm(landmarks, "LEFT")
            #loose_right, right_angle = detect_loose_upper_arm(landmarks, "RIGHT") # right_angle is not used

            # Store and Display results (COMMENTED OUT FOR SERVER EXECUTION)
            #cv2.putText(image, f"Left Loose: {'Yes' if loose_left else 'No'} ({int(left_angle)}°)",
            #            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            #cv2.putText(image, f"Right Loose: {'Yes' if loose_right else 'No'} ({int(right_angle)}°)",
            #            (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

            results_list.append({"Left Loose": 'Yes' if loose_left else 'No', "Left Angle": int(left_angle)})
        else:
            print("No human detected.", file=sys.stderr) # Printing the results that server will retrieve from the script

        #cv2.imshow("Bicep Curl Analysis", image) # Comment out image display code for server execution

    cap.release()
    #cv2.destroyAllWindows() # Comment out image display code for server execution
    print(f"Bicep Analysis Results: {results_list}")