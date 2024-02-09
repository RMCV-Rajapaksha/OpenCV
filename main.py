import cv2
import math
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1200)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

colorR = (0, 255, 0)

class DragRectangle():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def updatePos(self, cursor):
        cx, cy = cursor[0], cursor[1]
        self.posCenter = (cx, cy)

rectList = []
for x in range(5):
    rectList.append(DragRectangle([((x * 150) + 250), 150]))

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
        index_finger = lmList[8]  # Index finger tip landmark
        middle_finger = lmList[12]  # Middle finger tip landmark

        # Calculate the distance between the index and middle finger using Euclidean distance
        distance = math.sqrt((middle_finger[0] - index_finger[0]) ** 2 + (middle_finger[1] - index_finger[1]) ** 2)

        print(f"Distance between index and middle finger: {distance}")
        if distance < 35:
            cursor = lmList[8]  # Index finger tip landmark
            # Call the function update
            for rect in rectList:
                rect.updatePos(cursor)

    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size

        # Draw a semi-transparent rectangle on the image
        rect_color = colorR
        rect_alpha = 0.5  # Set the transparency (0.0 - fully transparent, 1.0 - fully opaque)
        overlay = img.copy()
        cv2.rectangle(overlay, (int(cx - w // 2), int(cy - h // 2)), (int(cx + w // 2), int(cy + h // 2)), rect_color, cv2.FILLED)
        img = cv2.addWeighted(overlay, rect_alpha, img, 1 - rect_alpha, 0)

    # Display the image
    display_window_name = "Image"
    cv2.imshow(display_window_name, img)

    # Wait for a key press
    key_pressed = cv2.waitKey(1)
