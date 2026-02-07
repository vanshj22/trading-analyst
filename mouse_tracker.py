"""
Mouse Speed Tracker - Captures real mouse movement velocity
Install: pip install pynput
"""
from pynput import mouse
from datetime import datetime
import math

class MouseSpeedTracker:
    def __init__(self):
        self.positions = []
        self.speeds = []
        self.listener = None
        
    def start_tracking(self):
        """Start capturing mouse movements"""
        self.listener = mouse.Listener(on_move=self._on_move)
        self.listener.start()
    
    def stop_tracking(self):
        """Stop capturing"""
        if self.listener:
            self.listener.stop()
    
    def _on_move(self, x, y):
        """Called on every mouse movement"""
        timestamp = datetime.now()
        self.positions.append({'x': x, 'y': y, 'time': timestamp})
        
        # Keep only last 100 positions
        if len(self.positions) > 100:
            self.positions.pop(0)
        
        # Calculate speed if we have 2+ positions
        if len(self.positions) >= 2:
            self._calculate_speed()
    
    def _calculate_speed(self):
        """Calculate pixels per second"""
        p1 = self.positions[-2]
        p2 = self.positions[-1]
        
        # Distance in pixels
        distance = math.sqrt((p2['x'] - p1['x'])**2 + (p2['y'] - p1['y'])**2)
        
        # Time difference in seconds
        time_diff = (p2['time'] - p1['time']).total_seconds()
        
        if time_diff > 0:
            speed = distance / time_diff
            self.speeds.append(speed)
            
            # Keep only last 50 speeds
            if len(self.speeds) > 50:
                self.speeds.pop(0)
    
    def get_average_speed(self):
        """Get average mouse speed (pixels/second)"""
        if not self.speeds:
            return 0
        return sum(self.speeds) / len(self.speeds)
    
    def is_erratic(self, threshold=500):
        """Detect erratic mouse movement (panic indicator)"""
        avg_speed = self.get_average_speed()
        return avg_speed > threshold  # Fast = panic

# Usage example
if __name__ == "__main__":
    tracker = MouseSpeedTracker()
    tracker.start_tracking()
    
    import time
    print("Move your mouse around...")
    time.sleep(10)
    
    print(f"Average speed: {tracker.get_average_speed():.2f} pixels/sec")
    print(f"Erratic movement: {tracker.is_erratic()}")
    
    tracker.stop_tracking()
