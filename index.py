from tkinter import *;

from tkinter import ttk

import cv2;
import time;
import os

import mediapipe as mp

# import serial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils # it gives small dots onhands total 20 landmark points

    def findHands(self,img,draw=True):

        # Send rgb image to hands
        imgRGB = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

        self.results = self.hands.process(imgRGB)   #process the frame

        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    #Draw dots and connect them

                    self.mpDraw.draw_landmarks(img,handLms,
                    self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self,img, handNo=0, draw=True):
        """Lists the position/type of landmarks
        we give in the list and in the list ww have stored
        type and position of the landmarks.
        List has all the lm position"""

        lmlist = []

        # check wether any landmark was detected
        if self.results.multi_hand_landmarks:
            #Which hand are we talking about
            myHand = self.results.multi_hand_landmarks[handNo]
            # Get id number and landmark information
            for id, lm in enumerate(myHand.landmark):
                # id will give id of landmark in exact index number
                # height width and channel
                h,w,c = img.shape
                #find the position
                cx,cy = int(lm.x*w), int(lm.y*h) #center
                # print(id,cx,cy)
                lmlist.append([id,cx,cy])

                # Draw circle for 0th landmark
                if draw:
                    cv2.circle(img,(cx,cy), 15 , (255,0,255), cv2.FILLED)

        return lmlist




# Use a service account.
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "mlproject-7373c",
  "private_key_id": "aa2f63852b6e9f4ab7a88745a1e19f59c2947df6",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCxDm/piUgaohQI\n1QDCA3f/L0KM4Q+GhIHcJw9OabWRK8EGxO4pdGC4bio7odhOreydtcl6DzKR7y1W\nJWJfXlLcGA+ryw8bJ/RHNOZxmXNrWGioXe/qpSYDoEdQ/j5Z//NryRVjzoxm1tmx\nbXGQnvCYUTejdVv62A5bGxJkd/GOO9JV+V4we2rxLST0awWwq1C2zy2uw3lOicN7\n7MXu0KEgOW4psWL+Mw0FSpSe9ggUikwEk7ZtmsDBIuuqYBBRrblwwPZ2fnW6BGTi\njywQ6wrHNatwUwtbtVo2mI43vK468NSct+Pn00CbjyqfiCydf0/BsZf75rsNFOUQ\nIzjVclTRAgMBAAECggEABawMOsOKm0vQ731/YjfBOtwVOjUlja4mCNr5ew4Y4ncv\n3lsltA9F3/KriLCFIPQibeT6eN4OxS0P20AkWCDJ78IXkm3VZI3RngxcS4xabbht\n1eL4giBbSOd0EWyrq69u6WeON13REqRUYgI7DqKA26hSa3qhgTY1s4Z4/t32z5Me\nY3Vy8CqOA5QwPbyZ/jLGbYZuxWUiDiBAEa/k23aO+SGeqrFxKT9JNWL4earS+F1G\nqIKgcHJYxRbQh/TiUx2YUKqbXXwvYlvSELxH6+iFXOklM2xKhsxh/RdZ8/YG2JH9\nKl0OdRSYeMNJG/gaDtGFGbNMWktSiyJJVSXWI+aLdwKBgQDZr4jve41qm4B8rS0V\nFa/9/dEN/CGzGqjqwxUH9gtRW2+95dwo4EspXaqopsRK+1csU49xeKsF3n2Kvg42\n8S5wzEluDIAsG4bFmu6j0u960XdlXygOgQSyGtATVi4SfKJdlboJCOa8MHJ/DxZ2\nB98CgGGNDe0U6yUYiH3o/Aw5uwKBgQDQODsZVsw0I+aZC7JMM7tqGOkddoe/V8Ak\n/9AOCemn17y6Khd0cGaF3d0HBaGoOYsJCbBS+GBucM99+KU3sVle7KlHKxHAf8yl\nAPw1D2k1brNY1icnJ4T4KUa8r+63OkW3yspMfxPVpMFbe8/IJxVt2HZDMNWjJoer\n66v7r50s4wKBgQCeMkXWnDhyUB24/XU0zHUApVMm0aN/8JDvQuRmy7T/4+451/D+\nN7oHjs12EPO39h4s1XD6KpJHCqC7klDsNqvkR2HZuvXul/aCZoyku6dT3yPgpJ2M\npNBPytKKKugCgVbRofz3keN0wdSDZ+iP0DqOK9Q42PUBbb2grZirF3ie/wKBgHwf\nyTtFvt2mOSUrD9LVU/ffebgSnMG38dccmE6GIj/oH51q0iibiMJsjAJPnRrHktaE\nbBRJ9FJh9Y9G1lbo5jnsIs1GI4L5rGkAuVh4I2Oy5j8jCpwQtveow35f8pJPrpft\nz8LiTlShrpJ2sFrE0cV1sKpFRlXH9kDKcO/MtIm5AoGBAM9/FofHleGERSV9chwE\nt21H7LN1+nbus78LeGZRitB9FG3iGKq+oFumX+wuGr+4f+yVY5IKutalNrDlcKRM\nW7ljAzlBWjJzXUgAmawnBwOG9///zx5cYNNpIEDDYZ5CwF728UxWnYrb9lOiJ332\nMK3UQIy5LSoLkH5AmUBpRJDp\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-a3uhg@mlproject-7373c.iam.gserviceaccount.com",
  "client_id": "114418968262421496820",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-a3uhg%40mlproject-7373c.iam.gserviceaccount.com"
})

app = firebase_admin.initialize_app(cred)

db = firestore.client()
def ChangeData(data):
    doc_ref = db.collection(u'users').document(u'data')
    doc_ref.set({
        u'number': data,
    })   
def GetFrmData():
    doc_ref = db.collection(u'users').document(u'data')
    doc = doc_ref.get()
    return doc.to_dict()
  




# ser = serial.Serial("COM27", 9600, timeout = 1) #Change your port name COM... and your baudrate
# def receiveFingerData(fingerNum):
#     ser.write(str.encode(fingerNum))
#     print(fingerNum)


def mymainFun():
    wCam,hCam = 640,480

    cap = cv2.VideoCapture(0)
    cap.set(3,wCam);
    cap.set(4,hCam);

    # folderpath = "fingers";
    # myList = os.listdir(folderpath)
    # print(myList)
    # overlayList=[];
    # for imagepath in myList:
    #     image = cv2.imread(f'{folderpath}/{imagepath}');
    #     overlayList.append(image)
    # print(len(overlayList))
    pTime=0;

    detector = handDetector(detectionCon=0.75)
    tipsid = [4,8,12,16,20]
    while True:
        success, img = cap.read();

        img = detector.findHands(img)
        lmlist = detector.findPosition(img,draw=False)
        # print(lmlist)
        global totalFingerOpen
        totalFingerOpen=0
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
            print(GetFrmData())
            ChangeData(totalFingerOpen)
            # blutooth.receiveFingerData(totalFingerOpen)
            # h,w,c=overlayList[totalFingerOpen-1].shape;
            # img[0:h, 0:w] = overlayList[totalFingerOpen-1]

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime=cTime
        cv2.putText(img,f'{int(totalFingerOpen)}',(300,70), cv2.FONT_HERSHEY_PLAIN,3,(200,254,100))
        cv2.putText(img,f'For Quit Press q',(10,30), cv2.FONT_HERSHEY_PLAIN,1,(20,254,10))

        cv2.imshow("Image",img);
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
            
        if key == ord("q"):
            break
        

    # do a bit of cleanup
    cv2.destroyAllWindows()



root = Tk();
root.geometry("300x150+120+120")
frame = ttk.Frame(root,padding=10);



mynum = GetFrmData()
mynum =str(mynum['number'])
buttonStart = Button(frame, text="Start Project", bg="green",fg="white", command=mymainFun)

fingerLabel = Label(frame, text="Last Update:"+mynum, font=17)
print(mynum)




buttonStart.grid(row=0,column=1,pady=20)

fingerLabel.grid(row=1,column=1)


frame.pack();
root.mainloop()