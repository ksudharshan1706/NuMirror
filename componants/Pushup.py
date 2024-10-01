from componants.ExerciseInterface import ExerciseInterface
import cvzone
from cvzone.PoseModule import PoseDetector
import numpy as np
import cv2
pd = PoseDetector(trackCon=0.70,detectionCon=0.70)

count = 0
dir = 0
class Pushup(ExerciseInterface):
    def  __init__(self, name,poseCoordinates):
        super().__init__(name)
        self.poseCoordinates = poseCoordinates

    def angleCalculation(self,img,lmlist):
        #right Arm Angle
        RightArm = [lmlist[val][:-1] for val in [12,14,16]]
        self.rightArmAngle,img=pd.findAngle(RightArm[0],RightArm[1],RightArm[2],img)
        
        #left Arm Angle
        leftArm = [lmlist[val][:-1] for val in [15,13,11]]
        self.leftArmAngle,img = pd.findAngle(leftArm[0],leftArm[1],leftArm[2],img)

    def percentCalculation(self):
        #calculating the pushpup hand angle accuracy
        self.rightArmAccuracy = np.interp(self.rightArmAngle,(40,170),(0,100))
        self.leftArmAccuracy = np.interp(self.leftArmAngle,(40,170),(0,100))
        

    def Counter(self,img):
        global dir, count
        if self.rightArmAccuracy == 100 and self.leftArmAccuracy == 100:
            if dir == 0:
                count += 0.5
                dir = 1
        
        elif self.rightArmAccuracy  == 0 and self.leftArmAccuracy == 0:
            if dir == 1:
                count += 0.5
                dir = 0
        cv2.putText( img,str(int(count)),(50,100),cv2.FONT_HERSHEY_PLAIN,5,(255,0,0),5)
    

    # def getAngles(self,img, lmlist):
    #     return super().getAngles(img,lmlist, self.poseCoordinates)