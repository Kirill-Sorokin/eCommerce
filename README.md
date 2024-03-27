# Virtual T-Shirt Try-On Application
Welcome to the Virtual T-Shirt Try-On application! 
This project allows users to try on different t-shirts virtually using their device's camera. 
It uses OpenCV for image processing and MediaPipe for real-time pose detection.

# Features
- Real-time video capture from the webcam.
- Dynamic overlay of t-shirts based on the user's pose.
- Interactive UI to switch between different t-shirts.
- Gesture controls for a seamless try-on experience.

# Getting Started
*Prerequisites*
- Python 3.7 to 3.10
- OpenCV (opencv-python)
- MediaPipe
- cvzone

# Installation
*Clone the repository.*
*Set up a Python virtual environment:*
python3 -m venv venv
source venv/bin/activate

*Install the required packages:*
pip install opencv-python mediapipe cvzone

*Running the Application*
*Navigate to the project directory and run:*

# Troubleshooting
*Common Issues*
- MediaPipe Initialization Error: If you encounter an error related to MediaPipe graph configuration, ensure you're using a compatible version of Python. MediaPipe currently supports Python versions 3.7 to 3.10.
- Camera Access: Make sure your terminal or IDE has permission to use the camera on your device.
- Python Version Not Found: If you receive a command not found error for Python, verify that the correct version is installed and accessible in your PATH.

# Solutions
- Check your Python version with python --version.
- Use pyenv to manage multiple Python versions.
- Ensure your pyenv is correctly set up and initialized in your shell's configuration file.
- If you've updated or downgraded Python, reinstall the packages inside the virtual environment.

# Need Help?
*If you're facing issues that are not documented here, please:*
- Check the official MediaPipe documentation.
- Search through existing GitHub issues for similar problems.
- Please open a new issue in this repository with detailed information about the error and the steps you've taken.