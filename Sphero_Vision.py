import cv2
import numpy as np
import threading
import time


class SpheroVision:
    """Vision controller"""
    
    def __init__(self, camera_index=0):
        self.camera = None
        self.camera_index = camera_index
        
        # Red HSV range
        self.lower_red1 = np.array([0, 150, 100])
        self.upper_red1 = np.array([10, 255, 255])
        self.lower_red2 = np.array([170, 150, 100])
        self.upper_red2 = np.array([180, 255, 255])
        
        # Green HSV range
        self.lower_green = np.array([40, 100, 100])
        self.upper_green = np.array([80, 255, 255])
        
        # Detection parameters
        self.min_area = 500
        self.min_green_area = 200
        self.frame_width = 320
        self.frame_height = 240
        
        # Current results
        self.last_result = None
        self.is_tracking = False
        self.tracking_thread = None
    
    def initialize_camera(self):
        """Init camera"""
        try:
            self.camera = cv2.VideoCapture(self.camera_index)
            
            # Set resolution
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            
            # Test read
            ret, frame = self.camera.read()
            if not ret:
                print("Camera init failed")
                return False
            
            print(f"Camera ready ({self.frame_width}x{self.frame_height})")
            return True
            
        except Exception as e:
            print(f"Camera error: {e}")
            return False
    
    def release_camera(self):
        """Release camera"""
        if self.camera:
            self.camera.release()
            cv2.destroyAllWindows()
            print("Camera released")
    
    def detect_green_object(self, frame, hsv):
        """Detect Sphero LED"""
        # Green mask
        mask = cv2.inRange(hsv, self.lower_green, self.upper_green)
        
        # Morphology processing
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)
            
            if area > self.min_green_area:
                M = cv2.moments(largest)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    return (cx, cy), area
        
        return None, 0
    
    def detect_sphero_and_target(self, show_preview=False):
        """Detect both objects"""
        if not self.camera:
            return {'sphero_found': False, 'target_found': False}
        
        ret, frame = self.camera.read()
        if not ret:
            return {'sphero_found': False, 'target_found': False}
        
        # BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Detect Sphero
        sphero_pos, sphero_area = self.detect_green_object(frame, hsv)
        
        # Detect red target
        mask_red1 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        mask_red2 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        mask_red = mask_red1 | mask_red2
        
        # Morphology ops
        kernel = np.ones((5, 5), np.uint8)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
        
        # Find red contours
        contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        target_pos = None
        target_area = 0
        
        if contours:
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)
            
            if area > self.min_area:
                M = cv2.moments(largest)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    target_pos = (cx, cy)
                    target_area = area
        
        # Calculate positions
        result = {
            'sphero_found': sphero_pos is not None,
            'target_found': target_pos is not None,
            'sphero_pos': sphero_pos,
            'target_pos': target_pos
        }
        
        if sphero_pos and target_pos:
            # Vector calculation
            dx = target_pos[0] - sphero_pos[0]
            dy = target_pos[1] - sphero_pos[1]
            
            # Distance
            distance = (dx**2 + dy**2)**0.5
            
            # Angle calculation
            angle = np.degrees(np.arctan2(-dy, dx))
            
            result['relative_angle'] = angle
            result['distance'] = distance
            result['target_area'] = target_area
        
        # Preview window
        if show_preview:
            if sphero_pos:
                cv2.circle(frame, sphero_pos, 10, (0, 255, 0), 2)
                cv2.putText(frame, "Sphero", (sphero_pos[0]+15, sphero_pos[1]), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            if target_pos:
                cv2.circle(frame, target_pos, 10, (0, 0, 255), 2)
                cv2.putText(frame, "Target", (target_pos[0]+15, target_pos[1]), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            if sphero_pos and target_pos:
                # Draw line
                cv2.line(frame, sphero_pos, target_pos, (0, 255, 0), 2)
                # Show info
                mid_x = (sphero_pos[0] + target_pos[0]) // 2
                mid_y = (sphero_pos[1] + target_pos[1]) // 2
                cv2.putText(frame, f"{result['relative_angle']:.0f}deg {result['distance']:.0f}px", 
                           (mid_x, mid_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            cv2.imshow('Sphero Vision', frame)
            cv2.waitKey(1)
        
        return result
    
    def detect_red_object(self, show_preview=False):
        """Detect red only"""
        if not self.camera:
            return {'found': False}
        
        ret, frame = self.camera.read()
        if not ret:
            return {'found': False}
        
        # HSV conversion
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Red mask
        mask1 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        mask2 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        mask = mask1 | mask2
        
        # Denoise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        result = {'found': False}
        
        if contours:
            # Largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            if area > self.min_area:
                # Center point
                M = cv2.moments(largest_contour)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    
                    # Center offset
                    center_x = self.frame_width / 2
                    offset = cx - center_x
                    
                    # Normalized angle
                    angle_offset = offset / center_x
                    
                    result = {
                        'found': True,
                        'offset': offset,
                        'area': area,
                        'position': (cx, cy),
                        'angle': angle_offset
                    }
                    
                    # Draw preview
                    if show_preview:
                        cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
                        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
                        cv2.line(frame, (int(center_x), 0), (int(center_x), self.frame_height), (255, 0, 0), 1)
        
        # Show windows
        if show_preview:
            cv2.imshow('Red Detection', frame)
            cv2.imshow('Mask', mask)
            cv2.waitKey(1)
        
        self.last_result = result
        return result
    
    def start_tracking(self, callback=None, show_preview=False):
        """Start tracking loop"""
        if self.is_tracking:
            print("Already tracking")
            return
        
        self.is_tracking = True
        
        def track_loop():
            while self.is_tracking:
                result = self.detect_red_object(show_preview=show_preview)
                if callback and result['found']:
                    callback(result)
                time.sleep(0.1)
        
        self.tracking_thread = threading.Thread(target=track_loop, daemon=True)
        self.tracking_thread.start()
        
        print("Tracking started")
    
    def stop_tracking(self):
        """Stop tracking"""
        self.is_tracking = False
        if self.tracking_thread:
            self.tracking_thread.join(timeout=1)
        print("Tracking stopped")


# Test code
if __name__ == "__main__":
    print("="*60)
    print(" "*20 + "Vision Test")
    print("="*60)
    print("\nPrepare red object")
    print("Press 'q' to quit\n")
    
    vision = SpheroVision()
    
    if not vision.initialize_camera():
        print("Camera failed")
        exit()
    
    print("Detecting red...\n")
    
    try:
        while True:
            result = vision.detect_red_object(show_preview=True)
            
            if result['found']:
                print(f"Found red: "
                      f"pos=({result['position'][0]}, {result['position'][1]}), "
                      f"offset={result['offset']:.1f}px, "
                      f"angle={result['angle']:+.2f}, "
                      f"area={result['area']:.0f}")
            else:
                print("No red detected")
            
            # Press 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nInterrupted")
    
    vision.release_camera()
    print("\nTest complete")

