import time
import threading
from spherov2.types import Color

class SpheroProgrammedMovement:
    def __init__(self, api):
        self.api = api
        self.is_running = False
    
    def move_forward(self, duration=1.0):
        try:
            speed = 30
            self.api.set_speed(speed)
            time.sleep(duration)
            self.api.set_speed(0)
        except Exception as e:
            print(f"fail: {e}")
    
    def turn_left(self, duration=1.0):
        try:
            speed = 30
            current_heading = self.api.get_heading()
            self.api.set_heading(current_heading - 90)
            self.api.set_speed(speed)
            time.sleep(duration)
            self.api.set_speed(0)
        except Exception as e:
            print(f"fail: {e}")
    
    def turn_right(self, duration=1.0):
        try:
            speed = 30
            current_heading = self.api.get_heading()
            self.api.set_heading(current_heading + 90)
            self.api.set_speed(speed)
            time.sleep(duration)
            self.api.set_speed(0)
        except Exception as e:
            print(f"fail: {e}")
    
    def wait(self, duration=1.0):
        time.sleep(duration)
    
    def triangle_route(self):
        try:
            
            self.api.set_heading(0)
            
            self.move_forward(1)
            self.wait(0.3)
            
            self.api.set_heading(120)
            self.move_forward(1)
            self.wait(0.3)
            
            #self.api.set_heading(240)
            #self.move_forward(1)
            #self.wait(0.5)
            
            self.api.set_heading(0)
            print("triangle completed")
            
        except Exception as e:
            print(f"fail: {e}")
    
    def forward_roll_sequence(self):
        try:
            speed = 30
            print("start forward roll")
            self.api.set_speed(speed)
            self.api.set_heading(0)  # 向前
            time.sleep(4.0)
            self.api.set_speed(0)
            print("forward roll completed")
        except Exception as e:
            print(f"fail: {e}")
    
    def backward_roll_sequence(self):
        try:
            speed = 30
            print("start backward roll")
            self.api.set_speed(speed)
            self.api.set_heading(180)  # 向后
            time.sleep(5.0)
            self.api.set_speed(0)
            print("backward roll completed")
        except Exception as e:
            print(f"fail: {e}")

    def spin_sequence(self):
        """spin"""
        try:
            print("start spin")
            self.api.spin(720, 7)
            print("spin completed")
        except Exception as e:
            print(f"fail: {e}")
    
    def execute_program(self):
        if self.is_running:
            print("programmed movement is running")
            return
        
        self.is_running = True
        print("\n" + "="*50)
        print("start programmed movement")
        print("="*50)
        
        try:
            self.triangle_route()
            self.wait(1.0)
            
            self.forward_roll_sequence()
            self.wait(1.0)
            
            self.backward_roll_sequence()
            self.wait(1.0)
            
            self.spin_sequence()
            self.wait(1.0)
            
            print("programmed movement sequence completed")
            
        except Exception as e:
            print(f"fail: {e}")
        finally:
            self.is_running = False
            try:
                self.api.set_speed(0)
            except:
                pass
    
    def start_program_async(self):
        if self.is_running:
            print("programmed movement is running")
            return
        
        thread = threading.Thread(target=self.execute_program, daemon=True)
        thread.start()
        print("programmed movement started in background")
    
    def stop_program(self):
        self.is_running = False
        try:
            self.api.set_speed(0)
            print("programmed movement stopped")
        except:
            pass
