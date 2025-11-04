import time
import threading
import random
from pynput import keyboard
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
from Sphero_Pattern import SpheroPattern
from Sphero_Voice import SpheroVoiceRecognition


class SpheroStateMachine:
    """state machine"""
    
    def __init__(self):
        self.toy = None
        self.api = None
        self.patterns = SpheroPattern()
        self.voice = SpheroVoiceRecognition()
        
        # state
        self.current_state = "SLEEP"
        self.is_running = True
        self.should_stop = False
        
        # timers
        self.state_start_time = time.time()
        self.patrol_duration = 60
        self.angry_duration = 30
        
        # collisions
        self.collision_count = 0
        self.max_collisions = 5
        
        # q-learning
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.3
        
        # keyboard
        self.keyboard_listener = None
        
        # shake detect
        self.last_orientation = None
        self.shake_threshold = 0.3
        
        # alt collision
        self.last_speed = 0
        self.speed_change_threshold = 20
        self.collision_check_interval = 0.1
        self.last_collision_check = 0
        
        # breathing led
        self.breathing_thread = None
        self.breathing_active = False
        
    def connect(self):
        """connect"""
        try:
            print("Searching device...")
            self.toy = scanner.find_toy(toy_name="SB-D96A")
            if not self.toy:
                print("Device not found")
                return False
            
            self.api = SpheroEduAPI(self.toy)
            self.api.__enter__()
            
            # collision on
            self.setup_collision_detection()
            
            time.sleep(1)
            print(f"Connected: {self.toy.name}")
            return True
        except Exception as e:
            print(f"Connect failed: {e}")
            return False
    
    def setup_collision_detection(self):
        """collision setup"""
        try:
            # enable
            self.api.enable_collision_detection()
            # callback
            self.api.on_collision = self.on_collision_detected
            print("Collision on")
        except Exception as e:
            print(f"Collision setup failed: {e}")
            print("use fallback")
    
    def on_collision_detected(self, collision_data):
        """on collision"""
        self.collision_count += 1
        print(f"Collision! count={self.collision_count}")
        
        # stop
        self.api.stop_roll()
        
        # led red
        self.api.set_main_led(Color(255, 0, 0))
        
        # threshold
        if self.current_state == "PATROL" and self.collision_count >= self.max_collisions:
            self.transition_to_state("ANGRY")
        else:
            # delay
            time.sleep(0.5)
            self.api.set_main_led(Color(255, 255, 255))
    
    def check_collision_alternative(self):
        """disabled"""
        # disabled
        return False
    
    def detect_shake(self):
        """shake detect"""
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
            
            return total_change > self.shake_threshold
        except Exception:
            return False
    
    def start_breathing_effect(self, color, duration=0.5):
        """breathing led"""
        if self.breathing_active:
            return
        
        self.breathing_active = True
        
        def breathing_loop():
            while self.breathing_active:
                try:
                    # fade in
                    for brightness in range(0, 255, 10):
                        if not self.breathing_active:
                            break
                        led_color = Color(
                            int(color[0] * brightness / 255),
                            int(color[1] * brightness / 255),
                            int(color[2] * brightness / 255)
                        )
                        self.api.set_front_led(led_color)
                        self.api.set_back_led(led_color)
                        time.sleep(duration / 50)
                    
                    # fade out
                    for brightness in range(255, 0, -10):
                        if not self.breathing_active:
                            break
                        led_color = Color(
                            int(color[0] * brightness / 255),
                            int(color[1] * brightness / 255),
                            int(color[2] * brightness / 255)
                        )
                        self.api.set_front_led(led_color)
                        self.api.set_back_led(led_color)
                        time.sleep(duration / 50)
                except Exception as e:
                    print(f"呼吸灯效果错误: {e}")
                    break
        
        self.breathing_thread = threading.Thread(target=breathing_loop, daemon=True)
        self.breathing_thread.start()
    
    def stop_breathing_effect(self):
        """stop breathing"""
        self.breathing_active = False
        if self.breathing_thread:
            self.breathing_thread.join(timeout=1)
    
    def transition_to_state(self, new_state):
        """switch state"""
        print(f"State: {self.current_state} -> {new_state}")
        
        # stop current
        self.stop_current_state_behavior()
        
        # set state
        self.current_state = new_state
        self.state_start_time = time.time()
        
        # reset vars
        if new_state == "PATROL":
            self.collision_count = 0
        
        # start state
        self.start_state_behavior()
    
    def stop_current_state_behavior(self):
        """stop state"""
        if not self.api:
            return
            
        if self.current_state == "PATROL":
            self.api.set_speed(0)
        elif self.current_state == "ANGRY":
            self.api.set_speed(0)
        elif self.current_state in ["SLEEP", "SATISFIED"]:
            self.stop_breathing_effect()
    
    def start_state_behavior(self):
        """start state"""
        if not self.api:
            return
            
        if self.current_state == "PATROL":
            self.patterns.show_expression(self.api, "wave")
            self.start_patrol()
        elif self.current_state == "SLEEP":
            self.patterns.show_expression(self.api, "sleep")
            self.start_breathing_effect((255, 255, 255), 1.0)
        elif self.current_state == "ANGRY":
            self.patterns.show_expression(self.api, "angry")
            self.start_angry_behavior()
        elif self.current_state == "INTERACT":
            self.api.set_speed(0)
            self.patterns.show_expression(self.api, "ishmael")
        elif self.current_state == "SATISFIED":
            self.api.set_speed(0)
            self.patterns.show_expression(self.api, "satisfied")
            self.start_breathing_effect((220, 80, 0), 0.8)
    
    def start_patrol(self):
        """start patrol"""
        def patrol_loop():
            while self.current_state == "PATROL" and self.is_running and not self.should_stop:
                try:
                    # choose action
                    action = self.choose_patrol_action()
                    self.execute_patrol_action(action)
                    # wait finish
                    time.sleep(2.5)
                except Exception as e:
                    print(f"Patrol error: {e}")
                    time.sleep(0.5)
        
        patrol_thread = threading.Thread(target=patrol_loop, daemon=True)
        patrol_thread.start()
    
    def choose_patrol_action(self):
        """pick action"""
        actions = [
            (0, 40),
            (0, 40),
            (0, 40),
            (45, 30),
            (315, 30),
            (90, 25),
            (270, 25),
            (135, 20),
            (225, 20),
            (180, 15),
        ]
        
        # bias forward
        if random.random() < 0.7:
            # forward set
            forward_actions = [action for action in actions if action[0] == 0]
            return random.choice(forward_actions)
        else:
            # others
            other_actions = [action for action in actions if action[0] != 0]
            return random.choice(other_actions)
    
    def execute_patrol_action(self, action):
        """exec action"""
        heading, speed = action
        try:
            # longer move
            duration = 2.0
            self.api.roll(heading, speed, duration)
        except Exception as e:
            print(f"Action error: {e}")
    
    def start_angry_behavior(self):
        """angry spin"""
        def angry_loop():
            while self.current_state == "ANGRY" and self.is_running and not self.should_stop:
                try:
                    # spin
                    self.api.spin(360, 2)
                    time.sleep(0.5)
                except Exception as e:
                    print(f"Angry error: {e}")
                    time.sleep(0.5)
        
        angry_thread = threading.Thread(target=angry_loop, daemon=True)
        angry_thread.start()
    
    def on_key_press(self, key):
        """key input"""
        try:
            if key == keyboard.Key.esc:
                print("ESC stop...")
                self.should_stop = True
                self.is_running = False
                return False
            
            elif hasattr(key, 'char') and key.char:
                if key.char.lower() == 'r':
                    if self.current_state in ["INTERACT", "SATISFIED"]:
                        self.transition_to_state("PATROL")
                
                elif key.char.lower() == 's':
                    if self.current_state in ["PATROL", "ANGRY", "SATISFIED"]:
                        self.transition_to_state("INTERACT")
                
                elif key.char.lower() == 'q':
                    if self.current_state == "INTERACT":
                        self.transition_to_state("SLEEP")
                
                elif key.char.lower() == 'x':
                    print("X stop...")
                    self.should_stop = True
                    self.is_running = False
                    return False
        
        except AttributeError:
            pass
    
    def on_voice_detected(self):
        """voice hit"""
        print("Voice: your fault")
        self.transition_to_state("ANGRY")
    
    def check_state_transitions(self):
        """tick"""
        current_time = time.time()
        state_duration = current_time - self.state_start_time
        
        # patrol check
        if self.current_state == "PATROL":
            # patrol timeout
            if state_duration >= self.patrol_duration:
                self.transition_to_state("SLEEP")
            
            # alt collision
            self.check_collision_alternative()
        
        elif self.current_state == "ANGRY":
            # angry timeout
            if state_duration >= self.angry_duration:
                self.transition_to_state("SLEEP")
        
        elif self.current_state == "INTERACT":
            # interact timeout
            if state_duration >= 30:
                self.transition_to_state("SLEEP")
        
        elif self.current_state == "SATISFIED":
            # satisfy timeout
            if state_duration >= 20:
                self.transition_to_state("SLEEP")
        
        # shake
        if self.detect_shake():
            if self.current_state in ["SLEEP", "ANGRY"]:
                self.transition_to_state("SATISFIED")
    
    def run(self):
        """run"""
        print("="*60)
        print(" "*20 + "Sphero FSM")
        print("="*60)
        print("Keys:")
        print("  R - patrol")
        print("  S - interact")
        print("  Q - sleep")
        print("  X - stop now")
        print("  ESC - quit")
        print("  shake - satisfy")
        print("  voice 'your fault' - angry")
        print("="*60)
        
        # voice on
        self.voice.start_listening(callback=self.on_voice_detected)
        
        # keys on
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()
        
        # start state
        self.start_state_behavior()
        
        try:
            # loop
            while self.is_running and not self.should_stop:
                self.check_state_transitions()
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\nInterrupted")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """cleanup"""
        print("Cleaning up...")
        
        # stop all
        if self.api:
            try:
                self.stop_current_state_behavior()
            except Exception as e:
                print(f"Stop error: {e}")
        
        # voice off
        if self.voice:
            self.voice.stop_listening()
        
        # keys off
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
        # stop robot
        if self.api:
            try:
                # stop
                self.api.set_speed(0)
                print("✓ stop")
                
                # clear led
                self.api.clear_matrix()
                print("✓ clear matrix")
                
                # leds off
                self.api.set_front_led(Color(0, 0, 0))
                self.api.set_back_led(Color(0, 0, 0))
                print("✓ leds off")
                
                # reset
                self.api.set_heading(0)
                print("✓ reset heading")
                
            except Exception as e:
                print(f"Cleanup error: {e}")
        
        # disconnect
        if self.api:
            try:
                self.api.__exit__(None, None, None)
                print("✓ disconnected")
            except Exception as e:
                print(f"Disconnect error: {e}")
        
        print("Cleanup done")


def main():
    """main"""
    state_machine = SpheroStateMachine()
    
    if state_machine.connect():
        try:
            state_machine.run()
        except Exception as e:
            print(f"Run error: {e}")
        finally:
            state_machine.cleanup()
    else:
        print("Connect failed")


if __name__ == "__main__":
    main()
