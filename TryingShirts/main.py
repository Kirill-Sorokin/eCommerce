import os
import cv2
import cvzone
from cvzone.PoseModule import PoseDetector

# Initialize camera capture; '0' indicates the default camera (typically the built-in webcam)
capture = cv2.VideoCapture(0)

# Initialize the pose detector from cvzone.
detector = PoseDetector()

# Path to the folder containing the shirt images for virtual try-on.
shirtFolderPath = "shirts"
listShirts = [file for file in os.listdir(shirtFolderPath) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Constants for shirt resizing based on pose detection.
fixedRatio = 262 / 190  # widthOfShirt/widthOfPoint11to12
shirtRatioHeightWidth = 581 / 440
imageNumber = 0

# Load buttons for UI interaction from the correct path.
imgButtonRight = cv2.imread("TryingShirts/button/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)

counterRight = 0
counterLeft = 0
selectionSpeed = 10

while True:
    success, img = capture.read()
    if not success:
        print("Failed to capture image")
        break

    # Apply pose detection on the captured frame.
    img = detector.findPose(img, draw=False)  # No drawing for skeleton
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

    if lmList:
        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]
        imgShirt = cv2.imread(f"{shirtFolderPath}/{listShirts[imageNumber]}", cv2.IMREAD_UNCHANGED)

        widthOfShirt = int(abs(lm11[0] - lm12[0]) * fixedRatio)
        imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
        currentScale = abs(lm11[0] - lm12[0]) / 190
        offset = int(44 * currentScale), int(48 * currentScale)

        try:
            # Overlay the resized shirt image onto the user's frame.
            img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
        except Exception as e:
            print(f"Error overlaying shirt: {e}")

        # Overlay navigation buttons onto the frame.
        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        # Interaction for changing the shirt selection based on pose gestures.
        if lmList[16][1] < 300:  # Right hand gesture
            counterRight += 1
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber < len(listShirts) - 1:
                    imageNumber += 1

        elif lmList[15][1] > 900:  # Left hand gesture
            counterLeft += 1
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1

        else:
            counterRight = 0
            counterLeft = 0

    cv2.imshow("Virtual T-Shirt Try-On", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and destroy all OpenCV windows.
capture.release()
cv2.destroyAllWindows()