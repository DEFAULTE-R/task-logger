import subprocess
from datetime import datetime

def get_timestamp():
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")

def get_active_window():
    try:
        win_id = subprocess.check_output(
            ["xdotool", "getactivewindow"]
        ).decode().strip()

        win_name = subprocess.check_output(
            ["xdotool", "getwindowname", win_id]
        ).decode().strip()

        return {
            "window_id": win_id,
            "window_name": win_name,
            "timestamp": get_timestamp()
        }
    except Exception as e:
        return {
            "window_name": "unknown",
            "error": str(e),
            "timestamp": get_timestamp()
        }
