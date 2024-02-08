import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1200)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
colorR = (0, 255, 0)
cx,cy,w,h= 100,100,200,200

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip the image
    if not success:
        break

    lmList = []  # Initialize lmList to an empty list

    hands, img = detector.findHands(img)  # Detect the hands
    if hands:
        lmList = hands[0]['lmList']  # Extract landmarks from the first detected hand
        # You can use lmList for further processing

    if lmList:
        cursor = lmList[8]  # Index finger tip landmark
        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            colorR = (255, 0, 0)
           # cx, cy = cursor
        else:
            colorR = (0, 255, 0)

    # Draw a filled rectangle on the image
    cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED)

    # Display the image
    cv2.imshow("Image", img)

    # Wait for a key press
    cv2.waitKey(1)