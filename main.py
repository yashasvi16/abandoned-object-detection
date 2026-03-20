import cv2
import argparse
import imutils
from src.background_sub import StaticBackgroundSubtractor
from src.tracker import AbandonedObjectTracker

def main(video_path, bg_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video source {video_path}")
        return

    subtractor = StaticBackgroundSubtractor(diff_threshold=25, canny_low=30, canny_high=150)
    tracker = AbandonedObjectTracker(min_area=1000, static_frame_threshold=60) 

    # NEW: Load the clean background image if provided
    if bg_path:
        bg_img = cv2.imread(bg_path)
        if bg_img is None:
            print(f"Error: Could not load background image at {bg_path}")
            return
        
        bg_img = imutils.resize(bg_img, width=640)
        gray_bg = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)
        gray_bg = cv2.GaussianBlur(gray_bg, (5, 5), 0)
        subtractor.set_reference_frame(gray_bg)
        print(f"[INFO] Loaded static reference frame from {bg_path}")
    else:
        print("[WARNING] No background image provided. Will auto-capture frame 1.")

    print("Starting video stream. Press 'q' to quit.")
    frame_count = 0 

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Video stream ended.")
            break

        frame = imutils.resize(frame, width=640)
        display_frame = frame.copy() 

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

        # Fallback if no image was provided
        if frame_count == 0 and not bg_path:
            subtractor.set_reference_frame(gray_frame)
            print("Auto-captured frame 1 as reference background.")
        
        thresh, edges = subtractor.apply(gray_frame)

        if thresh is not None and edges is not None:
            display_frame = tracker.update(thresh, display_frame)
            cv2.imshow("Threshold", thresh)
            cv2.imshow("Canny Edges", edges)

        cv2.imshow("Surveillance Feed", display_frame)

        frame_count += 1

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Abandoned Object Detection Pipeline")
    parser.add_argument("-v", "--video", type=str, required=True, help="Path to the video file")
    # Added an argument for the background image
    parser.add_argument("-b", "--background", type=str, default=None, help="Path to the empty background image")
    args = parser.parse_args()

    main(args.video, args.background)