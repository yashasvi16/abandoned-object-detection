import cv2
import numpy as np

class StaticBackgroundSubtractor:
    def __init__(self, diff_threshold=25, canny_low=30, canny_high=150):
        self.reference_frame = None
        self.diff_threshold = diff_threshold
        
        # Thresholds for Canny Edge Detection
        self.canny_low = canny_low
        self.canny_high = canny_high

    def set_reference_frame(self, frame):
        """
        Sets the static background frame. 
        Expects a grayscale, blurred frame.
        """
        self.reference_frame = frame

    def apply(self, current_frame):
        """
        Compares the current frame to the reference frame, extracts the differential,
        and applies Canny edge detection.
        """
        if self.reference_frame is None:
            return None, None

        # 1. Compute the absolute difference between current frame and reference frame
        frame_diff = cv2.absdiff(self.reference_frame, current_frame)

        # 2. Threshold the difference to binarize the image (isolate the new objects)
        _, thresh = cv2.threshold(frame_diff, self.diff_threshold, 255, cv2.THRESH_BINARY)

        # 3. Dilate the thresholded image to fill in holes (makes contours more solid)
        thresh = cv2.dilate(thresh, None, iterations=2)

        # 4. Apply Canny Edge Detection to the thresholded image to isolate boundaries
        edges = cv2.Canny(thresh, self.canny_low, self.canny_high)

        return thresh, edges