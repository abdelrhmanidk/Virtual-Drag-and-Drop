import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

# Initialize the HandDetector with a detection confidence of 0.8
detector = HandDetector(detectionCon=0.8)

# Capture video from the webcam (camera index 1)
cap = cv2.VideoCapture(1)

# Set the width and height of the video capture
cap.set(3, 1280)
cap.set(4, 720)

coloR = (255, 0, 0)

cx, cy, w, h = 100, 100, 200, 200




class DragRect():
    def __init__(self, posCenter,size=[200,200]):
        self.posCenter = posCenter
        self.size = size
    def update(self,cursor):
            cx,cy = self.posCenter
            w,h = self.size
        # Check if the cursor is within the rectangle
            if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
                # coloR = (0, 255, 0)  # Change color to green if inside rectangle
                self.posCenter = cursor[:2]  # Update the center of the rectangle
rectList = []
for x in range(5):
     
    rectList.append( DragRect([x*250+150,150]))

while True: 
    success, img = cap.read()  # Capture a frame from the webcam
    img = cv2.flip(img, 1)  # Flip the image horizontally

    if not success:
        break  # If frame is not captured correctly, exit the loop

    # Detect hands in the image and draw landmarks
    hands, img = detector.findHands(img, draw=True)

    if hands:
        # Get the first hand's landmark list (lmList)
        lmList = hands[0]['lmList']  # Landmark list for the first hand

        # Get the positions of the index finger tip (landmark 8) and middle finger tip (landmark 12)
        p1 = lmList[8][:2]  # (x, y) of index finger tip
        p2 = lmList[12][:2]  # (x, y) of middle finger tip

        # Calculate the distance between index and middle finger tips
        l, _, _ = detector.findDistance(p1, p2, img)
        print(l)
        if l < 70:

            # Get the position of the index finger tip (landmark 8)
            cursor = lmList[8]
            # call the update
            for rect in rectList:

                rect.update(cursor)
    # for rect in rectList:
    #             cx,cy = rect.posCenter
    #             w,h = rect.size

    #             # # Check if the cursor is within the rectangle
    #             # if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
    #             #     coloR = (0, 255, 0)  # Change color to green if inside rectangle
    #             #     cx, cy = cursor[:2]  # Update the center of the rectangle
    #             # else:
    #             #     coloR = (255, 0, 0)  # Reset color to red if outside rectangle

    #     # Draw the rectangle after hand detection
    #             cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), coloR, cv2.FILLED)
    #             cvzone.cornerRect(img,(cx - w // 2, cy - h // 2, w, h),20,rt=0)


    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
                cx,cy = rect.posCenter
                w,h = rect.size
                cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), coloR, cv2.FILLED)
                cvzone.cornerRect(imgNew,(cx - w // 2, cy - h // 2, w, h),20,rt=0)
    out = img.copy()
    alpha = 0.3
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img,alpha,imgNew,1 - alpha,0)[mask]   


    # Display the image with hand landmarks
    cv2.imshow("Image", out)

    # Wait for 1 millisecond; this allows for a smooth video stream
    cv2.waitKey(1) 