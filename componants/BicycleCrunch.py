from componants.ExerciseInterface import ExerciseInterface
import cvzone
from cvzone.PoseModule import PoseDetector
import numpy as np
import cv2
pd = PoseDetector(trackCon=0.70,detectionCon=0.70)

count = 0
dir = 0
class BicycleCrunch(ExerciseInterface):
    def __init__(self, name,poseCoordinates):
        super().__init__(name)
        self.poseCoordinates = poseCoordinates
    
    def angleCalculation(self,img,lmlist):
        RightLeg = [lmlist[val][:-1] for val in [24,26,28]]
        self.RightLegAngle,img=pd.findAngle(RightLeg[0],RightLeg[1],RightLeg[2],img)
        
        #left Arm Angle
        leftLeg = [lmlist[val][:-1] for val in [23,25,27]]
        self.leftLegAngle,img = pd.findAngle(leftLeg[0],leftLeg[1],leftLeg[2],img)


    def percentCalculation(self):
        #calculating the pushpup hand angle accuracy
        self.rightLegAccuracy = np.interp(self.RightLegAngle,(45,165),(0,100))
        self.leftLegAccuracy = np.interp(self.leftLegAngle,(45,165),(0,100))
        print(self.rightLegAccuracy,self.leftLegAccuracy)
    
    def Counter(self,img):
        global dir, count
        if self.rightLegAccuracy > 98 and self.leftLegAccuracy < 3:
            if dir == 0:
                count += 0.5
                dir = 1
        
        elif self.rightLegAccuracy  < 3 and self.leftLegAccuracy > 98:
            if dir == 1:
                count += 0.5
                dir = 0
        cv2.putText( img,str(int(count)),(50,100),cv2.FONT_HERSHEY_PLAIN,5,(255,0,0),5)