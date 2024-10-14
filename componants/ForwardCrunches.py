from componants.ExerciseInterface import ExerciseInterface
import cvzone
from cvzone.PoseModule import PoseDetector
import numpy as np
import cv2
pd = PoseDetector(trackCon=0.70,detectionCon=0.70)

count = 0
dir = 0
class ForwardCrunches(ExerciseInterface):
    def __init__(self,name,poseCoordinates):
        super().__init__(name)
        self.poseCoordinates = poseCoordinates
    
    def angleCalculation(self,img,lmlist):
        crunchright = [lmlist[val][:-1] for val in [26,24,12]]
        self.crunchrightAngle,img=pd.findAngle(crunchright[0],crunchright[1],crunchright[2],img)
        
        #left Arm Angle
        crunchLeft = [lmlist[val][:-1] for val in [25,23,11]]
        self.crunchLeftAngle,img = pd.findAngle(crunchLeft[0],crunchLeft[1],crunchLeft[2],img)


    def percentCalculation(self):
        #calculating the pushpup hand angle accuracy
        self.rightCrunchAccuracy = np.interp(self.crunchrightAngle,(45,165),(0,100))
        self.leftCrunchAccuracy = np.interp(self.crunchLeftAngle,(45,165),(0,100))
        print(self.rightCrunchAccuracy,self.leftCrunchAccuracy)
    
    def Counter(self,img):
        pass
        # global dir, count
        # if self.rightLegAccuracy > 98 and self.leftLegAccuracy < 3:
        #     if dir == 0:
        #         count += 0.5
        #         dir = 1
        
        # elif self.rightLegAccuracy  < 3 and self.leftLegAccuracy > 98:
        #     if dir == 1:
        #         count += 0.5
        #         dir = 0
        # cv2.putText( img,str(int(count)),(50,100),cv2.FONT_HERSHEY_PLAIN,5,(255,0,0),5)