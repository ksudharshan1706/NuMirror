from abc import ABC, abstractmethod

import cv2
class ExerciseInterface(ABC):
    poseCoordinates = []
    def  __init__(self, name,reps=30):
        self.name = name
    
    @abstractmethod
    def angleCalculation(self,coordinates):
        pass

    @abstractmethod
    def Counter(self):
        pass

    @abstractmethod
    def percentCalculation(self):
        pass
    
    # @abstractmethod
    # def getAngles(self,img,lmlist,Coordinates):
    #     _CoordinatesLength = len(Coordinates)
    #     poseCoordinates = [lmlist[val][:-1] for val in Coordinates]
    #     for (cx,cy) in poseCoordinates:
    #         cv2.circle(img,(cx,cy),10,(0,255,255),-1)
    #     for i in range(_CoordinatesLength-1):
    #         cv2.line(img,poseCoordinates[i],poseCoordinates[i+1],(0,0,255),6)

