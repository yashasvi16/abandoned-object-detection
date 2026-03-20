# Abandoned Object Detection using Canny Edge Detection

An automated computer vision surveillance pipeline engineered to detect and track unattended anomalous objects in video streams. 

This project utilizes spatial-temporal tracking and background subtraction architecture to monitor contour stasis, triggering automated security alarms when an item remains stationary beyond predefined thresholds.

## Features & Architecture

* **Background Subtraction Architecture:** Converts RGB video streams to grayscale, applies Gaussian blurring to reduce high-frequency noise, and computes real-time frame differentials against a static reference frame.
* **Algorithmic Feature Extraction:** Implements the Canny Edge Detection algorithm to isolate object boundaries and generate highly accurate spatial contours.
* **Temporal Tracking Mechanism:** Utilizes custom centroid tracking and Euclidean distance calculations to monitor object stasis over predefined frame thresholds (e.g., 60 consecutive frames).
* **Automated Alert System:** Dynamically updates tracking bounding boxes from "Tracking" (Green) to "ALARM" (Red) upon confirming an abandoned object.

## Tech Stack
* **Python 3.x**
* **OpenCV (`opencv-python`)**: Core computer vision algorithms, background subtraction, and edge detection.
* **NumPy**: Matrix operations and image array handling.
* **Imutils**: Convenience functions for aspect-aware resizing.

## Project Structure
\`\`\`text
abandoned-object-detection/
│
├── data/                       # Contains test videos and reference frames
│   ├── Surveillance_Video.avi
│   └── First_Frame.png
│
├── src/                        # Core algorithmic modules
│   ├── __init__.py
│   ├── background_sub.py       # Differential computation & Canny Edge logic
│   └── tracker.py              # Temporal stasis and centroid tracking logic
│
├── main.py                     # Execution pipeline and video ingestion
└── requirements.txt            # Dependency locking
\`\`\`

## Installation & Setup

1. **Clone the repository:**
   \`\`\`bash
   git clone https://github.com/yourusername/abandoned-object-detection.git
   cd abandoned-object-detection
   \`\`\`

2. **Create a virtual environment and install dependencies:**
   \`\`\`bash
   python -m venv venv
   # Activate: venv\Scripts\activate (Windows) or source venv/bin/activate (Mac/Linux)
   pip install -r requirements.txt
   \`\`\`

## Usage

**Run with a Pre-Captured Background (Recommended for Surveillance Data):**
Provide both the video feed and a clean, empty reference frame to initialize the background subtractor.
\`\`\`bash
python main.py -v data/Surveillance_Video.avi -b data/First_Frame.png
\`\`\`

**Run with Live Webcam / Auto-Capture:**
Point the camera at a static scene. The script will automatically capture the very first frame as the clean background, or press \`r\` at any time to manually reset the reference frame.
\`\`\`bash
python main.py -v 0
\`\`\`