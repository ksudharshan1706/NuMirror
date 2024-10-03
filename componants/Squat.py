from componants.ExerciseInterface import ExerciseInterface
import cvzone
from cvzone.PoseModule import PoseDetector
import numpy as np
import cv2
pd = PoseDetector(trackCon=0.70,detectionCon=0.70)

count = 0
dir = 0
class Squat(ExerciseInterface):
        def  __init__(self, name,poseCoordinates):
            super().__init__(name)
            self.poseCoordinates = poseCoordinates
        
        def angleCalculation(self,img,lmlist):
        #right Leg Angle
            RightLeg = [lmlist[val][:-1] for val in [28,26,24]]
            self.rightLegAngle,img=pd.findAngle(RightLeg[0],RightLeg[1],RightLeg[2],img)
            
            #left Leg Angle
            leftLeg = [lmlist[val][:-1] for val in [23,25,27]]
            self.leftLegAngle,img = pd.findAngle(leftLeg[0],leftLeg[1],leftLeg[2],img)
            
        def percentCalculation(self):
            #calculating the squat hand angle accuracy
            self.rightLegAccuracy = np.interp(self.rightLegAngle,(215,330),(0,100))
            self.leftLegAccuracy = np.interp(self.leftLegAngle,(215,330),(0,100))
            

        def Counter(self,img):
            global dir, count
            if self.rightLegAccuracy == 100 and self.leftLegAccuracy == 100:
                if dir == 0:
                    count += 0.5
                    dir = 1
            
            elif self.rightLegAccuracy  == 0 and self.leftLegAccuracy == 0:
                if dir == 1:
                    count += 0.5
                    dir = 0
            cv2.putText( img,str(int(count)),(50,100),cv2.FONT_HERSHEY_PLAIN,5,(255,0,0),5)
        

        # def getAngles(self,img, lmlist):
        #     return super().getAngles(img,lmlist, self.poseCoordinates)