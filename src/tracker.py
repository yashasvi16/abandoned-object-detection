import cv2
import math

class AbandonedObjectTracker:
    def __init__(self, min_area=500, static_frame_threshold=50, distance_tolerance=20):
        self.min_area = min_area
        self.static_frame_threshold = static_frame_threshold
        self.distance_tolerance = distance_tolerance
        self.tracked_objects = {}
        self.next_object_id = 0

    def _calculate_distance(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def update(self, thresh_frame, original_frame):
        contours, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        current_centroids = []
        current_bboxes = []

        for c in contours:
            if cv2.contourArea(c) < self.min_area:
                continue
                
            x, y, w, h = cv2.boundingRect(c)
            cx = x + w // 2
            cy = y + h // 2
            
            current_centroids.append((cx, cy))
            current_bboxes.append((x, y, w, h))

        updated_tracked_objects = {}
        
        for i, centroid in enumerate(current_centroids):
            matched_id = None
            
            for obj_id, obj_data in self.tracked_objects.items():
                dist = self._calculate_distance(centroid, obj_data['centroid'])
                if dist < self.distance_tolerance:
                    matched_id = obj_id
                    break
            
            if matched_id is not None:
                static_count = self.tracked_objects[matched_id]['static_count'] + 1
                updated_tracked_objects[matched_id] = {
                    'centroid': centroid,
                    'bbox': current_bboxes[i],
                    'static_count': static_count
                }
            else:
                updated_tracked_objects[self.next_object_id] = {
                    'centroid': centroid,
                    'bbox': current_bboxes[i],
                    'static_count': 0
                }
                self.next_object_id += 1

        self.tracked_objects = updated_tracked_objects
        
        for obj_id, obj_data in self.tracked_objects.items():
            x, y, w, h = obj_data['bbox']
            static_count = obj_data['static_count']
            
            if static_count >= self.static_frame_threshold:
                color = (0, 0, 255) 
                label = f"ALARM! Abandoned Obj"
                cv2.putText(original_frame, "SECURITY ALERT: ABANDONED ITEM DETECTED", 
                            (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            else:
                color = (0, 255, 0) 
                label = f"Tracking..."
                
            cv2.rectangle(original_frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(original_frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return original_frame