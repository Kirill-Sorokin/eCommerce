import cvzone, cv2
from cvzone.PoseModule import PoseDetector

# If using a pre-recorded video: 
# capture = cv2.VideoCapture("Resources/Videos/....")
capture = cv2.VideoCapture(0)
detector = PoseDetector()

while True:
    success, img = capture.read()
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboWithHands = False)
    if bboxInfo:
        # center = bboxInfo["center"]
        # cv2.circle(img, center, 5, (160, 32, 240), cv2.FILLED)


    cv2.imshow("Image", img)
    cv2.waitKey(1)