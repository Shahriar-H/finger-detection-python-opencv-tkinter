import cv2;
import time;
import os
import HandTrackingModule as htm

import blutooth
def mymainFun():
    wCam,hCam = 640,480

    cap = cv2.VideoCapture(0)
    cap.set(3,wCam);
    cap.set(4,hCam);

    folderpath = "fingers";
    myList = os.listdir(folderpath)
    # print(myList)
    overlayList=[];
    for imagepath in myList:
        image = cv2.imread(f'{folderpath}/{imagepath}');
        overlayList.append(image)
    print(len(overlayList))
    pTime=0;

    detector = htm.handDetector(detectionCon=0.75)
    tipsid = [4,8,12,16,20]
    while True:
        success, img = cap.read();

        img = detector.findHands(img)
        lmlist = detector.findPosition(img,draw=False)
        # print(lmlist)

        if len(lmlist) != 0:
            fingersArr=[];
            # Thumb Finger
            if lmlist[tipsid[0]][1] > lmlist[tipsid[0]-1][1]:
                fingersArr.append(1)
            else:
                fingersArr.append(0)

            # Rest 4 Fingers
            for id in range(1,5):
                if lmlist[tipsid[id]][2] < lmlist[tipsid[id]-2][2]:
                    fingersArr.append(1)
                else:
                    fingersArr.append(0)
            #print(fingersArr)
            totalFingerOpen = fingersArr.count(1);
            print(totalFingerOpen)
            # fire.ChangeData(totalFingerOpen)
            # blutooth.receiveFingerData(totalFingerOpen)
            h,w,c=overlayList[totalFingerOpen-1].shape;
            img[0:h, 0:w] = overlayList[totalFingerOpen-1]

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime=cTime
        cv2.putText(img,f'FPS: {int(fps)}',(300,70), cv2.FONT_HERSHEY_PLAIN,3,(200,254,100))
        cv2.putText(img,f'For Quit Press q',(10,30), cv2.FONT_HERSHEY_PLAIN,1,(20,254,10))

        cv2.imshow("Image",img);
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()