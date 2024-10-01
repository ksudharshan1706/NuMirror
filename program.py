import cv2
import numpy as np
import cvzone
from cvzone.PoseModule import PoseDetector
import math
from enum import Enum
from componants.ExerciseInterface import ExerciseInterface
from componants.Pushup import Pushup
from componants.Squat import Squat


class ExcerciseForm(Enum):
    PUSHUP = 1
    SQUAT = 2
    PLANK = 3

# vid_red = cv2.VideoCapture("pushup.mp4")
vid_red = cv2.VideoCapture("squats2.mp4")
# vid_red = cv2.VideoCapture(0)
pd = PoseDetector(trackCon=0.70,detectionCon=0.70)
dir = 0
count = 0

print("Excercise type : ")
Excersize = input().upper()

while 1:
    ret,img = vid_red.read()
    if not ret:
        vid_red = cv2.VideoCapture("squats2.mp4")
        # vid_red = cv2.VideoCapture("pushup.mp4")
        # vid_red = cv2.VideoCapture(0)
        continue
    pd.findPose(img,draw=0)
    img = cv2.resize(img,(1000,500))
    selected_exercise = ExcerciseForm[Excersize]
    lmlist,bbox = pd.findPosition(img,draw=0,bboxWithHands=0)

    
    if(selected_exercise == ExcerciseForm.PUSHUP):
        pushup = Pushup("pushup",[16,14,12,11,13,15])
        pushup.angleCalculation(img,lmlist)  # Output: Angle calculated for PushUp
        pushup.percentCalculation()
        pushup.Counter(img)

    # elif selected_exercise == ExcerciseForm.PLANK:
    #     ExerciseInterface.getAngles(img,lmlist,[28,26,24,12,14,16,11,13,15,23,25,27])
    elif selected_exercise == ExcerciseForm.SQUAT :
        squat = Squat("squat",[28,26,24,23,25,27])
        squat.angleCalculation(img,lmlist)  # Output: Angle calculated for PushUp
        squat.percentCalculation()
        squat.Counter(img)

    cv2.imshow("webview",img)
    cv2.waitKey(1)
