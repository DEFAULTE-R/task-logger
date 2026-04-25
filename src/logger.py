import time
from datetime import datetime
from PIL import Image
import numpy as np
import os

from src.capture import capture_screen
import src.database as db


def image_difference(path1, path2):
    try:
        img1 = Image.open(path1).resize((200, 200))
        img2 = Image.open(path2).resize((200, 200))

        arr1 = np.array(img1)
        arr2 = np.array(img2)

        diff = np.mean(np.abs(arr1 - arr2))
        return diff
    except:
        return 999


def infer_label(path):
    try:
        img = Image.open(path).resize((100, 100))
        arr = np.array(img)

        brightness = np.mean(arr)
        variance = np.var(arr)

        # Heuristics
        if brightness < 40:
            return "idle"
        elif variance < 500:
            return "reading"
        elif brightness > 150:
            return "browsing"
        else:
            return "coding"

    except:
        return "unknown"


def log_loop(interval=1.0, threshold=5.0):
    print("[Logger] Smart capture + auto-labeling started...")

    session_id = db.create_session("smart_labeled_session")

    last_path = None

    while True:
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")

        shot = capture_screen()
        current_path = shot["path"]

        should_log = True

        if last_path:
            diff = image_difference(last_path, current_path)

            if diff < threshold:
                os.remove(current_path)
                should_log = False
            else:
                print(f"[Change] diff={diff:.2f}")

        if should_log:
            label = infer_label(current_path)

            db.insert_action(
                session_id=session_id,
                timestamp=ts,
                action_type="screen_change",
                detail=f"auto:{label}",
                x=0,
                y=0,
                screenshot_before=last_path,
                screenshot_after=current_path
            )

            last_path = current_path
            print(f"[Logged] {label}")

        time.sleep(interval)
