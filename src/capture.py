import time
import os
from datetime import datetime
import mss
import mss.tools

SAVE_DIR = "data/screens"

def ensure_dir():
    os.makedirs(SAVE_DIR, exist_ok=True)

def capture_screen():
    ensure_dir()

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{timestamp}.png"
    filepath = os.path.join(SAVE_DIR, filename)

    with mss.mss() as sct:
        monitor = sct.monitors[1]  # primary screen
        screenshot = sct.grab(monitor)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=filepath)

    return {
        "timestamp": timestamp,
        "path": filepath
    }

def run_capture_loop(interval=0.5):
    print("[Capture] Started...")

    while True:
        data = capture_screen()
        print(f"[Capture] Saved: {data['path']}")
        time.sleep(interval)
