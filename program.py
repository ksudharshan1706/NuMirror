import cv2
import numpy as np
import cvzone
from cvzone.PoseModule import PoseDetector
import math
from enum import Enum
from componants.ExerciseInterface import ExerciseInterface
from componants.Pushup import Pushup
from componants.Squat import Squat
from componants.BicycleCrunch import BicycleCrunch
from componants.ForwardCrunches import ForwardCrunches

class ExcerciseForm(Enum):
    PUSHUP = 1
    SQUAT = 2
    PLANK = 3
    CRUNCH = 4
    FORWARDCRUNCH = 5

# vid_red = cv2.VideoCapture("pushup.mp4")
vid_red = cv2.VideoCapture(0)
pd = PoseDetector(trackCon=0.70,detectionCon=0.70)
dir = 0
count = 0

print("Excercise type : ")
Excersize = input().upper()

while 1:
    ret,img = vid_red.read()
    if not ret:
        # vid_red = cv2.VideoCapture("pushup.mp4")
        vid_red = cv2.VideoCapture(0)
        continue
    pd.findPose(img,draw=0)
    img = cv2.resize(img,(1000,500))
    selected_exercise = ExcerciseForm[Excersize]
    lmlist,bbox = pd.findPosition(img,draw=0,bboxWithHands=0)
    if(len(lmlist) > 0):
        if selected_exercise == ExcerciseForm.PUSHUP:
            pushup = Pushup("pushup",[16,14,12,11,13,15])
            pushup.angleCalculation(img,lmlist)
            pushup.percentCalculation()
            pushup.Counter(img)

        elif selected_exercise == ExcerciseForm.SQUAT :
            squat = Squat("squat",[28,26,24,23,25,27])
            squat.angleCalculation(img,lmlist)
            squat.percentCalculation()
            squat.Counter(img)

        elif selected_exercise == ExcerciseForm.CRUNCH :
            _crunch = BicycleCrunch("Bicycle Crunch",[28,26,24,23,25,27])
            _crunch.angleCalculation(img,lmlist)
            _crunch.percentCalculation()
            _crunch.Counter(img)

        elif selected_exercise == ExcerciseForm.FORWARDCRUNCH :
            _forwardCrunch = ForwardCrunches("Forward Crunch",[12,24,26,11,23,25])
            _forwardCrunch.angleCalculation(img,lmlist)
            _forwardCrunch.percentCalculation()
            _forwardCrunch.Counter(img)

    cv2.imshow("NuMirror",img)
    cv2.waitKey(1)
