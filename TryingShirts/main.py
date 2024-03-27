import cvzone, cv2, os
from cvzone.PoseModule import PoseDetector

# Setup the camera capture. Using '0' to select the default webcam.
capture = cv2.VideoCapture(0)

# Initialize the pose detector from cvzone.
detector = PoseDetector()

# Path to the folder containing the shirt images for virtual try-on.
shirtFolderPath = "/workspaces/eCommerce-Trying-on-Shirts/TryingShirts/shirts"
# Obtain a list of shirt image filenames from the directory.
listShirts = os.listdir(shirtFolderPath)

# Constants for shirt resizing based on pose detection.
fixedRatio = 262 / 190  # Ratio based on shirt image and specific pose landmarks.
shirtRatioHeightWidth = 581 / 440  # Height-to-width ratio of the shirt image.
imageNumber = 0  # Index to keep track of the currently selected shirt.

# Load buttons for UI interaction.
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
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
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)

    if bboxInfo and lmList:
        # Calculate the new shirt width based on the distance between landmarks 11 and 12.
        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]
        widthOfShirt = int(abs(lm11[0] - lm12[0]) * fixedRatio)

        # Dynamically resize the shirt image based on the calculated width and predetermined ratios.
        try:
            imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
            offset = int(44 * (abs(lm11[0] - lm12[0]) / 190)), int(48 * (abs(lm11[0] - lm12[0]) / 190))

            # Overlay the resized shirt image onto the user's frame.
            img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
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