import time

try:
    import pyautogui
except Exception as import_error:
    print("pyautogui is not installed yet. Install requirements and run again.")
    print("Hint: open a terminal here and run: setup-venv (or) pip install -r requirements.txt")
    raise import_error


def main():
    print("Mouse jiggler started. Press Ctrl+C to stop.")
    dx = 10  # small movement in pixels
    delay_seconds = 2  # move every N seconds

    # Failsafe: moving mouse to a corner stops pyautogui by default.
    pyautogui.FAILSAFE = True

    toggle = True
    while True:
        try:
            # Get current position and nudge slightly left/right to avoid big jumps
            x, y = pyautogui.position()
            if toggle:
                pyautogui.moveTo(x + dx, y)
            else:
                pyautogui.moveTo(x - dx, y)
            toggle = not toggle
            time.sleep(delay_seconds)
        except KeyboardInterrupt:
            print("\nMouse jiggler stopped.")
            break


if __name__ == "__main__":
    main()




