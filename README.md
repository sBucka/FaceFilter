# FaceFilter

This project implements a simple face filter using Python and the OpenCV library. It uses pre-trained Haar Cascade classifiers to detect faces and eyes, and applies various filters like outlines, custom eyes, pupils, and nose modifications during live video capture.

## Features

- **Real-time face detection:** Identifies and outlines faces in the captured video.
- **Eye detection:** Detects both right and left eyes and can customize their appearance.
- **Nose filter:** Applies a circular overlay on the nose when certain conditions are met.
- **Dynamic color cycling:** Users can cycle through different colors for each filter feature.
- **Interactive controls:** Toggle and cycle filter options using keyboard commands.

## Dependencies

- Python 3.x
- OpenCV (`cv2`)
- Standard Python libraries: `math` and `enum`

## Setup Instructions

1. Ensure Python is installed on your system.
2. Install OpenCV if not already installed:
   - Run `pip install opencv-python`
3. Download the required Haar Cascade XML files:
   - `haarcascade_frontalface_default.xml` - face detection
   - `haarcascade_righteye_2splits.xml` - right eye detection
   - `haarcascade_lefteye_2splits.xml` - left eye detection
4. Place the XML files in the same directory as the Python script.

## Usage

- Run the Python script.
- The script will activate your webcam and open a window displaying the video feed.
- Use the following keyboard commands during runtime:
  - **Esc:** Exit the application.
  - **Space:** Change the outline color.
  - **0:** Toggle the face outline filter on or off.
  - **1:** Cycle the nose filter color.
  - **2:** Cycle the custom eyes filter color.
  - **3:** Cycle the pupils filter color.

## How It Works

- The script captures video frames from the webcam and converts them to grayscale.
- It detects faces and eyes using the pre-trained Haar Cascade classifiers.
- Filters are applied based on user interaction:
  - Toggling filters and cycling through colors based on key presses.
  - Drawing rectangles, circles, and text on the detected facial features.
- Color changes are managed via a dictionary mapping, and filters are toggled dynamically.
