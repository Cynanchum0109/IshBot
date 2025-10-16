import speech_recognition as sr
import threading
import time


class SpheroVoiceRecognition:
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        self.is_listening = False
        self.listen_thread = None
        
        self.target_phrase = "your fault"
        
        self.on_phrase_detected = None
    
    def start_listening(self, callback=None):
        """
        Args:
            callback: callback function when target phrase is detected
        """
        if self.is_listening:
            print("Voice listening is already running")
            return
        
        self.on_phrase_detected = callback
        self.is_listening = True
        
        # start background thread
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        
        print("Voice listening started (phrase: '{}')".format(self.target_phrase))
    
    def stop_listening(self):
        """stop voice listening"""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        print("Voice listening stopped")
    
    def _listen_loop(self):
        """background listening loop"""
        # initialize microphone
        with self.microphone as source:
            print("🎤 Calibrating microphone...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone ready\n")
            
            while self.is_listening:
                try:
                    # listen to audio (timeout 1 second)
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    # recognize speech
                    try:
                        text = self.recognizer.recognize_google(audio, language='en-US')
                        text_lower = text.lower()
                        
                        print(f"Recognized: {text}")
                        
                        if self.target_phrase in text_lower:
                            print(f"It's all your fault Ishmael!")
                            
                            if self.on_phrase_detected:
                                self.on_phrase_detected()
                        
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        print(f"Speech recognition service error: {e}")
                        time.sleep(1)
                
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    print(f"Listening error: {e}")
                    time.sleep(0.5)
    

