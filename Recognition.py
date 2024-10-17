import cv2
import mediapipe as mp
import numpy as np
import pyttsx3  # For voice output
from componants.Pushup import Pushup

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7,min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)  # First point (e.g., hip)
    b = np.array(b)  # Second point (e.g., knee)
    c = np.array(c)  # Third point (e.g., ankle)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Function to recognize squats or push-ups
def recognize_exercise(landmarks):
    # Extract necessary landmarks for squats and push-ups
    #Hip Landmarks
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    
    #Knee Landmarks
    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                 landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
    
    #Ankle Landmarks
    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
    right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                  landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

    #Shoulder Landmarks
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

    #Elbow Landmarks
    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                  landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    

    #Wrist Landmarks
    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                  landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]


    # Calculate left knee angle for squats and left elbow angle for push-ups
    left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
    left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

    # Calculate right knee angle for squats and right elbow angle for push-ups
    right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
    right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

    right_back_angle = calculate_angle(right_shoulder,right_hip,right_knee)
    left_back_angle = calculate_angle(left_shoulder,left_hip,left_knee)

    # print("right_back_angle",right_back_angle)
    # print("left_back_angle",left_back_angle)

    # Recognize squats based on knee angle
    if left_knee_angle < 75 and right_knee_angle < 75:
        return "Squats"
    # Recognize push-ups based on elbow angle
    elif left_elbow_angle < 50 and right_elbow_angle < 50 and right_back_angle > 175:
        return "Push ups"
    else:
        return None

# Initialize webcam
cap = cv2.VideoCapture(0)

# Start pose detection and exercise recognition
previous_Exercise = ""
while cap.isOpened():
    ret, frame = cap.read()
    # image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame)
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    frame = cv2.resize(frame,(1000,1000))
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Recognize the exercise
        exercise = recognize_exercise(results.pose_landmarks.landmark)

        if exercise and previous_Exercise != exercise:
                print(exercise,previous_Exercise,previous_Exercise != exercise)
                previous_Exercise = exercise
                # if  exercise == "Push ups":
                #     pushup = Pushup("pushup",[16,14,12,11,13,15])
                #     pushup.angleCalculation(frame,results.pose_landmarks.landmark)
                #     pushup.percentCalculation()
                #     pushup.Counter(img)
                # engine.say(exercise)
                # engine.runAndWait()

    cv2.imshow('Exercise Recognition', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
