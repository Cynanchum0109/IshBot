import time
import threading
from pynput import keyboard
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
from Sphero_Movement import SpheroMovement
from Sphero_Programmed_Movement import SpheroProgrammedMovement

class InteractiveSphero:
    def __init__(self):
        self.toy = None
        self.api = None
        self.is_running = True
        self.current_mode = "pattern"  
        
        self.palette = {
            "w": Color(255, 255, 255), 
            "o": Color(255, 115, 27),  
            "y": Color(255, 255, 0),   
            "b": Color(150, 100, 60), 
            "r": Color(255, 0, 0),        
            "0": None                    
        }
        
        # Ishoct
        self.pattern = [
            ["0","w","b","b","b","b","w","0"],
            ["w","o","o","o","o","o","o","w"],
            ["o","o","o","o","o","o","o","o"],
            ["o","o","y","o","o","y","o","o"],
            ["o","o","y","o","o","y","o","o"],
            ["o","o","o","b","b","o","o","o"],
            ["0","o","0","o","o","0","o","0"],
            ["o","o","0","o","o","0","o","o"]
        ]
        
        # angryish
        self.pickup_pattern = [
            ["0","w","b","b","b","b","w","0"],
            ["w","o","o","o","r","o","r","w"],
            ["o","o","o","r","r","o","r","r"],
            ["o","o","o","o","o","o","o","o"],
            ["o","o","o","r","r","o","r","r"],
            ["o","o","o","o","r","o","r","o"],
            ["0","o","0","o","o","0","o","0"],
            ["o","o","0","o","o","0","o","o"]
        ]
        
        # wave animation
        self.wave_frames = [
            [
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,1,1],
                [0,0,0,0,0,0,1,0],
                [0,0,0,0,1,1,1,0],
                [0,0,0,0,1,0,0,0],
                [0,0,1,1,1,0,0,0],
                [0,0,1,0,0,0,0,0],
                [1,1,1,0,0,0,0,0]
            ],
            [
                [0,0,0,0,0,0,1,0],
                [0,0,0,0,1,1,1,0],
                [0,0,0,0,1,0,0,0],
                [0,0,1,1,1,0,0,0],
                [0,0,1,0,0,0,0,0],
                [1,1,1,0,0,0,0,0],
                [1,0,0,0,0,0,0,0],
                [1,0,0,0,0,0,0,0]
            ]
        ]

        self.color_matrix = [[self.palette[cell] for cell in row] for row in self.pattern]
        self.pickup_color_matrix = [[self.palette[cell] for cell in row] for row in self.pickup_pattern]
        
        self.movement_controller = None
        self.programmed_movement = None
    
    def connect(self):
        try:
            print("Searching...")
            self.toy = scanner.find_toy(toy_name="SB-D96A")
            if not self.toy:
                print("Didn't find SB-D96A")
                return False
            
            print(f"Found {self.toy.name}")
            self.api = SpheroEduAPI(self.toy)
            self.api.__enter__()
            
            # initialize movement controller
            self.movement_controller = SpheroMovement(self.api)
            self.programmed_movement = SpheroProgrammedMovement(self.api)
            
            print("Connected")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def disconnect(self):
        """disconnect"""
        if self.api:
            try:
                self.api.__exit__(None, None, None)
                print("disconnect")
            except:
                pass
    
    def display_pattern(self):
        """Ishmael"""
        try:
            self.api.clear_matrix()
            
            for row in range(len(self.pattern)):
                for col in range(len(self.pattern[row])):
                    color = self.color_matrix[row][col]
                    if color is not None:
                        self.api.set_matrix_pixel(col, row, color)
            
            print("Ishmael")
        except Exception as e:
            print(f"fail: {e}")
    
    def display_pickup_pattern(self):
        """angry ishmael"""
        try:
            self.api.clear_matrix()
            
            for row in range(len(self.pickup_pattern)):
                for col in range(len(self.pickup_pattern[row])):
                    color = self.pickup_color_matrix[row][col]
                    if color is not None:
                        self.api.set_matrix_pixel(col, row, color)
            
            print("angry ishmael")
        except Exception as e:
            print(f"fail: {e}")
    
    def display_wave_animation(self):
        """wave animation"""
        print("wave animation")
        try:
            for _ in range(5):
                if self.current_mode != "wave": 
                    break
                    
                for frame in self.wave_frames:
                    if self.current_mode != "wave":
                        break
                        
                    # clear matrix
                    self.api.clear_matrix()
                    
                    # blue
                    for row in range(len(frame)):
                        for col in range(len(frame[row])):
                            if frame[row][col] == 1:
                                self.api.set_matrix_pixel(col, row, Color(0, 0, 255))
                    time.sleep(0.2)
                    
                    if self.current_mode != "wave":
                        break
                    
                    # white
                    for row in range(len(frame)):
                        for col in range(len(frame[row])):
                            if frame[row][col] == 1:
                                self.api.set_matrix_pixel(col, row, Color(255, 255, 255))
                    time.sleep(0.2)
            
            # default
            if self.current_mode == "wave":
                self.current_mode = "pattern"
                self.display_pattern()
                
        except Exception as e:
            print(f"fail: {e}")
    

    def on_key_press(self, key):
        try:
            if hasattr(key, 'char') and key.char:
                if key.char == 'w':  # wave
                    print("Wave animation")
                    self.current_mode = "wave"
                    threading.Thread(target=self.display_wave_animation, daemon=True).start()
                    
                elif key.char == 'p':
                    print("Ishmael")
                    self.current_mode = "pattern"
                    self.display_pattern()
                    
                elif key.char == 'q':
                    print("exit")
                    self.is_running = False
                    return False
                    
                elif key.char == 'm':
                    print("movement control")
                    threading.Thread(target=self.movement_controller.start_movement_control, daemon=True).start()
                    
                elif key.char == 'r':
                    print("HOLD ON TIGHT")
                    self.programmed_movement.start_program_async()
                    
                elif key.char == 's':
                    print("stop programmed movement")
                    self.programmed_movement.stop_program()
            
                    
        except AttributeError:
            pass
    
    def monitor_pickup(self):
        """monitor rotation"""
        try:
            # use gyroscope
            last_orientation = None
            
            while self.is_running:
                try:
                    orientation = self.api.get_quaternion()
                    
                    if last_orientation is not None:
                        q1, q2 = last_orientation, orientation
                        dot_product = abs(q1.w*q2.w + q1.x*q2.x + q1.y*q2.y + q1.z*q2.z)
                        
                        if dot_product < 0.95:
                            if self.current_mode != "pickup":
                                print("rotation detected")
                                self.current_mode = "pickup"
                                self.display_pickup_pattern()
                        else:
                            if self.current_mode == "pickup":
                                print("stable")
                                self.current_mode = "pattern"
                                self.display_pattern()
                    
                    last_orientation = orientation
                    time.sleep(0.2)
                    
                except Exception as e:
                    time.sleep(0.5)
                    continue
                    
        except Exception as e:
            print(f"fail: {e}")

    def start_interactive_mode(self):
        """interactive"""
        print("\n" + "="*50)
        print("interactive")
        print("="*50)
        print("control instructions:")
        print("   M  - start movement control")
        print("   R  - start programmed movement")
        print("   S  - stop programmed movement")
        print("   W  - wave animation")
        print("   P  - show ishmael")
        print("   Q  - exit")

        print("="*50)
        print("current display: default pattern")
        
        self.display_pattern()
        
        # start pickup monitor
        pickup_thread = threading.Thread(target=self.monitor_pickup, daemon=True)
        pickup_thread.start()
        
        # keyboard listener
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            try:
                while self.is_running:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("\ninterrupted")
            finally:
                listener.stop()
                self.disconnect()

def main():
    sphero = InteractiveSphero()
    
    if sphero.connect():
        try:
            sphero.start_interactive_mode()
        except Exception as e:
            print(f"program error: {e}")
        finally:
            sphero.disconnect()
    else:
        print(" Connection failed")

if __name__ == "__main__":
    main()

