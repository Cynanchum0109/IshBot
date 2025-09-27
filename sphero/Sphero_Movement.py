from pynput import keyboard

class SpheroMovement:
    def __init__(self, api):
        self.api = api
        
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.api.set_heading(0)

        self.listener = None
        self.is_running = False
    
    def on_press(self, key):
        # PRESS ESCAPE 'esc' TO EXIT PROGRAM
        if key == keyboard.Key.esc:
            return False
       
        speed = 30

        if key == keyboard.Key.up and not self.up_pressed:
            self.up_pressed = True
            self.api.set_speed(speed)           
        elif key == keyboard.Key.down and not self.down_pressed:
            self.down_pressed = True
            self.api.set_heading(self.api.get_heading()+180)
            self.api.set_speed(speed)           
        if key == keyboard.Key.left and not self.left_pressed:
            self.left_pressed = True
            self.api.set_heading(self.api.get_heading()-45)
        if key == keyboard.Key.right and not self.right_pressed:
            self.right_pressed = True
            self.api.set_heading(self.api.get_heading()+45)

    def on_release(self, key):
        if key == keyboard.Key.up:
            self.up_pressed = False
            self.api.set_speed(0)           
        elif key == keyboard.Key.down:
            self.down_pressed = False
            self.api.set_speed(0)           
        elif key == keyboard.Key.left:
            self.left_pressed = False        
        elif key == keyboard.Key.right:
            self.right_pressed = False
    
    def start_movement_control(self):
        """movement control"""
        if self.is_running:
            print("movement control is running")
            return
        
        self.is_running = True
        print("\n" + "="*40)
        print("movement control")
        print("="*40)
        print("control instructions:")
        print("   ↑  - forward")
        print("   ↓  - backward")
        print("   ←  - left")
        print("   →  - right")
        print("   ESC - exit")
        print("="*40)
        
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            try:
                listener.join()
            except KeyboardInterrupt:
                print("\ninterrupted")
            finally:
                self.is_running = False
    
    def stop_movement_control(self):
        """stop movement control"""
        self.is_running = False
        try:
            self.api.set_speed(0)
        except:
            pass
        print("movement control stopped")
