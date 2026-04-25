import time
from datetime import datetime

from src.capture import capture_screen
from src.window_tracker import get_active_window
import src.database as db


def log_loop(interval=1.0):
    print("[Logger] Starting real capture loop...")

    session_id = db.create_session("real_usage_session")

    last_screenshot = None

    while True:
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")

        # capture screenshot
        shot = capture_screen()

        # get active window
        win = get_active_window()

        # insert into DB as an action
        db.insert_action(
            session_id=session_id,
            timestamp=ts,
            action_type="window_activity",
            detail=win.get("window_name", "unknown"),
            x=0,
            y=0,
            screenshot_before=last_screenshot,
            screenshot_after=shot["path"],
        )

        last_screenshot = shot["path"]

        print(f"[Logger] Logged: {win.get('window_name')}")

        time.sleep(interval)
