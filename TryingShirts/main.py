import cv2
import os
from cvzone.PoseModule import PoseDetector

# Initialize camera capture; '0' indicates the default camera (typically the built-in webcam)
capture = cv2.VideoCapture(0)

# Initialize the pose detector from cvzone.
detector = PoseDetector()

# Path to the folder containing the shirt images for virtual try-on.
# Updated to use absolute path from the project root
shirtFolderPath = "shirts"  
# Obtain a list of shirt image filenames from the directory.
listShirts = [file for file in os.listdir(shirtFolderPath) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Constants for shirt resizing based on pose detection.
fixedRatio = 262 / 190  # Ratio based on shirt image and specific pose landmarks.
shirtRatioHeightWidth = 581 / 440  # Height-to-width ratio of the shirt image.
imageNumber = 0  # Index to keep track of the currently selected shirt.

# Load buttons for UI interaction.
# Updated to use the absolute path from the project root
imgButtonRight = cv2.imread("TryingShirts/button/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)

# Counters for button press simulation based on pose gestures.
counterRight = 0
counterLeft = 0
selectionSpeed = 10  # Controls the speed of changing shirts.

while True:
    success, img = capture.read()
    if not success:
        print("Failed to capture image")
        break

    # Apply pose detection on the captured frame.
    img = detector.findPose(img, draw=False)  # Added draw=False to prevent drawing the skeleton
    lmList, bboxInfo = detector.findPosition(img, draw=False)  # Added draw=False for the same reason

    if bboxInfo and lmList:
        # Calculate the new shirt width based on the distance between landmarks 11 and 12.
        lm11 = lmList[11]
        lm12 = lmList[12]
        widthOfShirt = int(abs(lm11[1] - lm12[1]) * fixedRatio)

        # Dynamically resize the shirt image based on the calculated width and predetermined ratios.
        try:
            imgShirt = cv2.imread(f"{shirtFolderPath}/{listShirts[imageNumber]}", cv2.IMREAD_UNCHANGED)
            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
            offset = int(44 * (abs(lm11[1] - lm12[1]) / 190)), int(48 * (abs(lm11[1] - lm12[1]) / 190))

            # Overlay the resized shirt image onto the user's frame.
            img = cvzone.overlayPNG(img, imgShirt, (lm12[1] - offset[0], lm12[2] - offset[1]))
        except Exception as e:
            print(f"Error overlaying shirt: {e}")

                # Overlay navigation buttons onto the frame.
        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        # Interaction for changing the shirt selection based on pose gestures.
        # Incrementing the right gesture counter if the right hand is raised.
        if lmList[16][1] < 300:  # Right hand gesture
            counterRight += 1
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber < len(listShirts) - 1:
                    imageNumber += 1

        # Incrementing the left gesture counter if the left hand is lowered.
        elif lmList[15][1] > 900:  # Left hand gesture
            counterLeft += 1
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1
        else:
            counterRight = 0
            counterLeft = 0

    # Display the processed frame.
    cv2.imshow("Virtual T-Shirt Try-On", img)

    # Break the loop and clean up on 'q' key press.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and destroy all OpenCV windows.
capture.release()
cv2.destroyAllWindows()

