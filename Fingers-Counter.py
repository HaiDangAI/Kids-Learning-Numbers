import cv2
import os
import time
import handTrackingModule as htm
def getNumber(ar):
    return ar.count(1) 

def main():
  wcam,hcam=640,480
  cap=cv2.VideoCapture(0)
  pTime=0
  detector = htm.handDetector(detectionCon=0.75)
  while True:
      success,img=cap.read()
      img = detector.findHands(img, draw=True )
      lmList=detector.findPosition(img,draw=False)
      #print(lmList)
      tipId=[4,8,12,16,20]
      if(len(lmList) != 0):
            fingers = []
            for i in range(5):
                TipToMcp = math.dist(lmList[tipId[i]][1:], lmList[mcpId[i]][1:])
                PipToMcp = math.dist(lmList[pipId[i]][1:], lmList[mcpId[i]][1:])
                if TipToMcp > PipToMcp:
                    fingers.append(1)
                else:
                    fingers.append(0)
            num = Finger_Counter.getNumber(fingers)
          
            
          cv2.rectangle(img,(20,255),(170,425),(0,255,0),cv2.FILLED)   
          cv2.putText(img,str(getNumber(fingers)),(45,375),cv2.FONT_HERSHEY_PLAIN,
                                      10,(255,0,0),20)  
          
      
      
      cTime=time.time()
      fps=1/(cTime-pTime)
      pTime=cTime
      cv2.putText(img, f'FPS: {int(fps)}',(400,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),3)
      cv2.imshow("image",img)
      if(cv2.waitKey(1) & 0xFF== ord('q')):
          break

if __name__ == "__main__":
    main()
