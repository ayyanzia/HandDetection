from time import ctime

import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode=False, maxHands=2,model_complexity = 1,detectionCon=0.5,trackCon=0.5):
        self.mode= mode
        self.maxHands =maxHands
        self.model_complexity = model_complexity
        self.detectionCon =detectionCon
        self.trackCon= trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,
                                        self.maxHands, self.model_complexity,self.detectionCon,self.trackCon,)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img, draw =True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        #detects landmarks

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    #position values to get find position
    def findPosition(self,img, handNo=0, draw =True):

        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand =self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                #print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmList.append([id, cx,cy])
                if draw:
                # find location of any point we want
                    cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

        return lmList

#to get positions of landmarks easily

def main ():
        pTime = 0
        ctime = 0
        cap = cv2.VideoCapture(1)
        img =detector =handDetector()
        while True:
            success, img = cap.read()
            img =detector.findHands(img)
            lmList=detector.findPosition(img)
            if len(lmList)!=0:
                print(lmList[4])
                #it will show index 4 which is Thumb Tip
                #Use can adjust for your point however you like

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 255), 3)

            #Shows the name of the program and passing it the img var
            cv2.imshow("Image", img)
            cv2.waitKey(1)


if __name__== "__main__":
    main()