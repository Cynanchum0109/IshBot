import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color

def main():
    toy = scanner.find_toy(toy_name="SB-D96A")  
    with SpheroEduAPI(toy) as api:
        try:
            api.clear_matrix()
            api.scroll_matrix_text("OK", Color(r=255, g=255, b=0), fps=10, wait=True)
        except Exception as e:
            api.set_main_led(Color(r=255, g=255, b=0))
            time.sleep(2)

if __name__ == "__main__":
    main()
