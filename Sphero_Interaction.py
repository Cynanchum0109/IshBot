import time
import os
from pynput import keyboard
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
from Sphero_Pattern import SpheroPattern
from Sphero_Voice import SpheroVoiceRecognition
from Sphero_Vision import SpheroVision


class SpheroInteraction:
    
    def __init__(self):
        self.toy = None
        self.api = None
        self.patterns = SpheroPattern()
        self.voice = SpheroVoiceRecognition()
        self.vision = SpheroVision()
        
        # state management
        self.current_state = "sleeping"  # sleeping, awake, idle, tracking
        self.is_running = True
        
        # orientation detection parameters
        self.last_orientation = None 
        self.wakeup_threshold = 0.2 
        
        # keyboard listener
        self.keyboard_listener = None
        
        # angry state
        self.angry_mode = False
        self.angry_start_time = None
        
        # tracking parameters
        self.tracking_speed = 60
        self.dead_zone = 50  

    def connect(self):
        try:
            print("Searching Sphero device...")
            self.toy = scanner.find_toy(toy_name="SB-D96A")
            if not self.toy:
                print("Didn't find SB-D96A")
                return False
            
            self.api = SpheroEduAPI(self.toy)
            self.api.__enter__()

            time.sleep(1)
            
            print(f"Connected to: {self.toy.name}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def disconnect(self):
        # stop visual tracking
        if self.vision:
            self.vision.stop_tracking()
            self.vision.release_camera()
        
        # stop voice listening
        if self.voice:
            self.voice.stop_listening()
        
        # stop keyboard listening
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
        # stop Sphero movement
        if self.api:
            try:
                self.api.set_speed(0)
            except:
                pass
        
        # disconnect Sphero
        if self.api:
            try:
                self.api.__exit__(None, None, None)
                print("EXIT")
            except:
                pass
    
    def on_key_press(self, key):
        try:
            if key == keyboard.Key.esc:
                self.is_running = False
                return False 
            
            elif hasattr(key, 'char') and key.char == 's':
                if self.current_state == "awake":
                    print("Press 's' for chasing")
                    self.current_state = "tracking"
                    green_color = Color(0, 255, 0)
                    self.api.set_front_led(green_color)
                    self.api.set_back_led(green_color)
                    print("LED set to green")
        except AttributeError:
            pass
    
    def trigger_angry(self):
        print("😠 ")
        
        self.angry_mode = True
        self.angry_start_time = time.time()
        
        # Stop Chasing
        if self.current_state == "tracking":
            self.api.set_speed(0)
        
        # Angry face
        self.patterns.show_expression(self.api, "angry")

        print("💢 ")
        self.api.spin(720, 1) 
    
    def navigate_to_target(self, result):
        if self.current_state != "tracking":
            return
        
        if self.angry_mode:
            return
    
        if result['target_found']:
            print("Detected red Whale, full speed ahead!")
            self.api.set_speed(self.tracking_speed)
        else:
            self.api.set_speed(0)
        
        # if not result['sphero_found']:
        #     print("Didn't find Sphero (green LED)")
        #     self.api.set_speed(0)
        #     return
        # 
        # if not result['target_found']:
        #     self.api.set_speed(0)
        #     return
        # 
        # angle = float(result['relative_angle'])
        # distance = float(result['distance'])
        # sphero_heading = int((90 - angle) % 360)
        # 
        # if distance > 150:
        #     speed = self.tracking_speed
        # elif distance > 80:
        #     speed = 15
        # else:
        #     speed = 0
        # 
        # if speed > 0:
        #     self.api.roll(sphero_heading, speed, 0.3)
        # else:
        #     self.api.set_speed(0)

    def play_wakeup_speech(self):
        try:
            speech_text = "Another day has begun, Let's get sailing."
            print(f"{speech_text}")
            os.system(f'say "{speech_text}" &') 
        except Exception as e:
            print(f" {e}")

    def wakeup_sequence(self):
        print("⏰ ")
        try:

            self.play_wakeup_speech()
            time.sleep(3)
            self.patterns.show_expression(self.api, "smile")

            self.patterns.show_expression(self.api, "ishmael")
            self.current_state = "awake"


        except Exception as e:
            print(f"{e}")


    def detect_wakeup(self):
        """orientation"""
        try:
            orient = self.api.get_orientation()
            if not orient:
                return False
            
            pitch = orient['pitch']
            roll = orient['roll']
            
            if self.last_orientation is None:
                self.last_orientation = (pitch, roll)
                return False
            
            last_pitch, last_roll = self.last_orientation
            delta_pitch = abs(pitch - last_pitch)
            delta_roll = abs(roll - last_roll)
            total_change = (delta_pitch**2 + delta_roll**2)**0.5
            
            self.last_orientation = (pitch, roll)
            
            if total_change > 0.2: 
                return True
            
            return False
        except Exception:
            return False

    def monitor_sleeping(self):

        print("\n💤 ")
        print("Shake or pick up to wake up\n")

        blink_state = False
        counter = 0

        while self.is_running and self.current_state == "sleeping":
            try:
                time.sleep(0.2)
                counter += 1

                if self.detect_wakeup():
                    self.wakeup_sequence()
                    break

                if counter % 10 == 0:
                    blink_state = not blink_state
                    brightness = 20 if blink_state else 0
                    self.api.set_front_led(Color(brightness, brightness, brightness))

            except Exception as e:
                print(f" {e}")
                time.sleep(0.5)
                continue

    def start_sleeping_mode(self):


        self.current_state = "sleeping"
        self.api.clear_matrix()
        self.api.set_front_led(Color(0, 0, 0))
        self.api.set_back_led(Color(0, 0, 0))

        # keyboard listener
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

        try:
            self.monitor_sleeping()
            if self.current_state == "awake":
                
                # initialize camera
                camera_ready = self.vision.initialize_camera()
                
                # start voice listening
                self.voice.start_listening(callback=self.trigger_angry)
                
                print("\nPress 's' to start tracking\n")
                
                # main loop
                while self.is_running:
                    if self.angry_mode and self.angry_start_time:
                        if time.time() - self.angry_start_time > 7:
                            print("😌 ")
                            self.angry_mode = False
                            self.patterns.show_expression(self.api, "ishmael")
                    
                    # tracking mode
                    if self.current_state == "tracking" and camera_ready:
                        result = self.vision.detect_sphero_and_target(show_preview=True)

                        self.navigate_to_target(result)
                    
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n\ninterrupted")
            self.is_running = False
        finally:
            self.disconnect()


def main():
   
    sphero = SpheroInteraction()
    if sphero.connect():
        try:
            sphero.start_sleeping_mode()
        except Exception as e:
            print(f"s {e}")
        finally:
            sphero.disconnect()
    else:
        print("Connection failed")


if __name__ == "__main__":
    main()
