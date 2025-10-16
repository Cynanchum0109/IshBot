import time
import threading
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
from Interactive_Sphero import InteractiveSphero


class SpheroHeartbeat:
    
    def __init__(self, api):
        self.api = api
        self.is_running = False
        self.heartbeat_thread = None
        
        self.bpm = 100
        self.beat_interval = 60.0 / self.bpm
        
        self.colors = {
            "bright_red": Color(255, 0, 0),
            "medium_red": Color(200, 0, 0),
            "dim_red": Color(80, 0, 0),
            "dark_red": Color(30, 0, 0),
            "off": Color(0, 0, 0)
        }
        
        self.timing = {
            "first_beat_up": 0.08,
            "first_beat_peak": 0.05,
            "first_beat_down": 0.08,
            "between_beats": 0.15,
            "second_beat_up": 0.07,
            "second_beat_peak": 0.04,
            "second_beat_down": 0.07,
            "rest": 0.46
        }
    
    
    def _lerp_color(self, color1, color2, t):
        r = int(color1.r + (color2.r - color1.r) * t)
        g = int(color1.g + (color2.g - color1.g) * t)
        b = int(color1.b + (color2.b - color1.b) * t)
        return Color(r, g, b)
    
    def _single_beat(self, intensity="strong"):
        if intensity == "strong":
            peak_color = self.colors["bright_red"]
            up_time = self.timing["first_beat_up"]
            peak_time = self.timing["first_beat_peak"]
            down_time = self.timing["first_beat_down"]
        else:
            peak_color = self.colors["medium_red"]
            up_time = self.timing["second_beat_up"]
            peak_time = self.timing["second_beat_peak"]
            down_time = self.timing["second_beat_down"]
        
        steps_up = 5
        for i in range(steps_up):
            if not self.is_running:
                return
            t = i / (steps_up - 1)
            color = self._lerp_color(self.colors["dark_red"], peak_color, t)
            self.api.set_front_led(color)
            time.sleep(up_time / steps_up)
        
        self.api.set_front_led(peak_color)
        time.sleep(peak_time)
        
        steps_down = 5
        for i in range(steps_down):
            if not self.is_running:
                return
            t = i / (steps_down - 1)
            color = self._lerp_color(peak_color, self.colors["dim_red"], t)
            self.api.set_front_led(color)
            time.sleep(down_time / steps_down)
    
    def _heartbeat_loop(self):
        print("Heartbeat started")
        self.api.set_front_led(self.colors["dark_red"])
        time.sleep(0.2)
        
        while self.is_running:
            self._single_beat("strong")
            if not self.is_running:
                break
            
            self.api.set_front_led(self.colors["dim_red"])
            time.sleep(self.timing["between_beats"])
            if not self.is_running:
                break
            
            self._single_beat("weak")
            if not self.is_running:
                break
            
            self.api.set_front_led(self.colors["dark_red"])
            time.sleep(self.timing["rest"])
        
        self.api.set_front_led(self.colors["off"])
        print("Heartbeat stopped")
    
    def start(self):
        if self.is_running:
            print("Already running")
            return
        
        self.is_running = True
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()
    
    def stop(self):
        if not self.is_running:
            return
        
        self.is_running = False
        if self.heartbeat_thread:
            self.heartbeat_thread.join(timeout=2.0)
        
        self.api.set_front_led(self.colors["off"])


class SpheroWave:
    
    def __init__(self, api):
        self.api = api
        self.is_running = False
        self.wave_thread = None
        
        self.colors = {
            "deep_blue": Color(0, 40, 80),
            "soft_white": Color(150, 180, 200),
            "off": Color(0, 0, 0)
        }
        
        self.timing = {
            "wave_up": 3.0,
            "wave_down": 3.0
        }
    
    def _lerp_color(self, color1, color2, t):
        r = int(color1.r + (color2.r - color1.r) * t)
        g = int(color1.g + (color2.g - color1.g) * t)
        b = int(color1.b + (color2.b - color1.b) * t)
        return Color(r, g, b)
    
    def _wave_cycle(self):
        steps = 30
        
        for i in range(steps):
            if not self.is_running:
                return
            t = i / (steps - 1)
            color = self._lerp_color(
                self.colors["deep_blue"], 
                self.colors["soft_white"], 
                t
            )
            self.api.set_front_led(color)
            time.sleep(self.timing["wave_up"] / steps)
        
        for i in range(steps):
            if not self.is_running:
                return
            t = i / (steps - 1)
            color = self._lerp_color(
                self.colors["soft_white"], 
                self.colors["deep_blue"], 
                t
            )
            self.api.set_front_led(color)
            time.sleep(self.timing["wave_down"] / steps)
    
    def _wave_loop(self):
        print("Wave started")
        self.api.set_front_led(self.colors["deep_blue"])
        time.sleep(0.5)
        
        while self.is_running:
            self._wave_cycle()
        
        self.api.set_front_led(self.colors["off"])
        print("Wave stopped")
    
    def start(self):
        if self.is_running:
            print("Already running")
            return
        
        self.is_running = True
        self.wave_thread = threading.Thread(target=self._wave_loop, daemon=True)
        self.wave_thread.start()
    
    def stop(self):
        if not self.is_running:
            return
        
        self.is_running = False
        if self.wave_thread:
            self.wave_thread.join(timeout=3.0)
        
        self.api.set_front_led(self.colors["off"])


def main():
    print("Searching...")
    toy = scanner.find_toy(toy_name="SB-D96A")
    
    if not toy:
        print("Not found")
        return
    
    print(f"Connected: {toy.name}")
    
    with SpheroEduAPI(toy) as api:
        heartbeat = SpheroHeartbeat(api)
        wave = SpheroWave(api)
        
        interactive = InteractiveSphero()
        interactive.toy = toy
        interactive.api = api
        
        interactive.display_pattern()
        
        print("\n" + "="*50)
        print("Sphero Light")
        print("="*50)
        print("Controls:")
        print("  h - Heartbeat")
        print("  w - Wave")
        print("  s - Stop")
        print("  q - Quit")
        print("="*50 + "\n")
        
        while True:
            choice = input("> ").strip().lower()
            
            if choice == 'h':
                wave.stop()
                heartbeat.stop()
                time.sleep(0.3)
                heartbeat.start()
                
            elif choice == 'w':
                heartbeat.stop()
                wave.stop()
                time.sleep(0.3)
                wave.start()
                
            elif choice == 's':
                heartbeat.stop()
                wave.stop()
                interactive.display_pattern()
                print("Stopped")
                
            elif choice == 'q':
                heartbeat.stop()
                wave.stop()
                api.clear_matrix()
                print("Quit")
                break
                
            else:
                print("Invalid")


if __name__ == "__main__":
    main()
