# 👁️ Abandoned Object Detection System

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/opencv--python-green.svg)](https://opencv.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Math-orange.svg)](https://numpy.org/)

An automated computer vision surveillance pipeline engineered to detect and track unattended anomalous objects in video streams in real-time. 

This project utilizes spatial-temporal tracking combined with a background subtraction architecture to monitor contour stasis. It dynamically triggers automated security alarms when an item remains stationary beyond predefined frame thresholds.

---

## ✨ Features & Architecture

* **Background Subtraction Architecture:** Converts RGB video streams to grayscale, applies Gaussian blurring to reduce high-frequency noise, and computes real-time absolute frame differentials against a static reference frame.
* **Algorithmic Feature Extraction:** Implements the **Canny Edge Detection** algorithm to isolate object boundaries and generate highly accurate spatial contours, ensuring robustness against environmental lighting changes and noise.
* **Temporal Tracking Mechanism:** Utilizes custom centroid tracking and Euclidean distance calculations (`math.hypot`) to monitor object stasis over predefined frame thresholds (e.g., `60` consecutive frames).
* **Automated Alert System:** Dynamically updates tracking bounding boxes and bounding box labels from "Tracking..." (Green) to "**ALARM! Abandoned Obj**" (Red) upon confirming an abandoned object. The console optionally alerts users.

---

## 🛠️ Tech Stack

* **Python 3.x**: Core application logic.
* **OpenCV (`opencv-python`)**: Core computer vision algorithms, absolute background subtraction, contour thresholding, and Canny edge detection mapping.
* **NumPy**: Under-the-hood fast matrix math operations and contiguous image array handling.
* **Imutils**: Convenience functions for aspect-aware image resizing and frame processing shortcuts.

---

## 🗂️ Project Structure

```text
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
├── Readme.md                   # Project documentation
└── requirements.txt            # Dependency locking
```

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/abandoned-object-detection.git
   cd abandoned-object-detection
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

The custom pipeline can be run in two primary modes: using a pre-captured background frame (ideal for pre-recorded surveillance datasets) or auto-capturing the background from a raw live feed.

### 1. Run with a Pre-Captured Background (Recommended)
Provide both the video feed and a clean, empty reference frame to explicitly initialize the static background subtractor.

```bash
python main.py -v data/Surveillance_Video.avi -b data/First_Frame.png
```

### 2. Run with Live Webcam / Auto-Capture
Point the camera at a static scene. The script will automatically capture the very **first frame** as the clean background reference.

```bash
python main.py -v 0
```

> **Note:** While the video stream is active, you can press the `q` key at any time to gracefully terminate the application and close all surveillance feed windows.

---

## 🧠 System Internals Configuration

If you need to tweak the detection sensitivities (e.g., adjusting the duration considered for an "abandoned" item), you can adjust the initialization parameters directly in `main.py`:

- **`StaticBackgroundSubtractor`:**
  - `diff_threshold` (Default `25`): Sensitivity for pixel differentiation relative to the reference.
  - `canny_low` (Default `30`): Lower bound limit for edge hysteresis mapping constraint.
  - `canny_high` (Default `150`): Upper bound limit for edge hysteresis mapping constraint.
- **`AbandonedObjectTracker`:**
  - `min_area` (Default `1000`): Minimum bounding box contour area to be considered a viable object footprint.
  - `static_frame_threshold` (Default `60`): Number of consecutive stasis frames required to trigger an alarm (approx `2` seconds at `30fps`).
  - `distance_tolerance` (Default `20`): Pixel distance radius variation allowed for grouping tracking object centroids across frames.