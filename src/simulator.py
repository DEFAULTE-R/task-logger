import random
import time
from datetime import datetime, timedelta
import src.database as db

ACTION_TYPES = [
    ("mouse_click", ["left_click", "right_click", "double_click"]),
    ("key_press", ["ctrl+c", "ctrl+v", "ctrl+s", "ctrl+z", "enter", "tab", "backspace"]),
    ("scroll", ["scroll_up", "scroll_down"]),
    ("drag", ["drag_start", "drag_end"]),
    ("type", ["text_input"]),
]

TEXT_SAMPLES = [
    "import pandas as pd",
    "def process_data(df):",
    "SELECT * FROM users WHERE",
    "git commit -m 'fix: update config'",
    "http://localhost:3000/api/",
    "npm run build",
    "docker-compose up -d",
]

def fake_screenshot_path(ts):
    return f"data/screens/{ts}.png"

def simulate_session(name="demo_session", num_actions=60):
    print(f"[Simulator] Creating session: {name}")
    session_id = db.create_session(name)

    base_time = datetime.utcnow()

    for i in range(num_actions):
        ts = (base_time + timedelta(seconds=i * 0.5)).strftime("%Y%m%d_%H%M%S_%f")
        action_type, details = random.choice(ACTION_TYPES)
        detail = random.choice(details)

        if action_type == "type":
            detail = random.choice(TEXT_SAMPLES)

        action = {
            "timestamp": ts,
            "action_type": action_type,
            "detail": detail,
            "x": random.randint(0, 1920),
            "y": random.randint(0, 1080),
            "screenshot_before": fake_screenshot_path(ts + "_before"),
            "screenshot_after": fake_screenshot_path(ts + "_after"),
        }

        db.insert_action(session_id, action)
        print(f"  [{i+1:02d}/{num_actions}] {action_type}: {detail}")
        time.sleep(0.02)

    print(f"[Simulator] Done. {num_actions} actions logged under session '{name}'")
    return session_id
