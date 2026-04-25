import random
from datetime import datetime
import src.database as db


def simulate_session(name="demo_session", num_actions=50):
    print(f"[Simulator] Creating session: {name}")

    session_id = db.create_session(name)

    action_types = ["mouse_click", "key_press", "scroll", "drag"]

    for _ in range(num_actions):
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")

        action_type = random.choice(action_types)

        detail = f"simulated_{action_type}"
        x = random.randint(0, 1920)
        y = random.randint(0, 1080)

        db.insert_action(
            session_id=session_id,
            timestamp=ts,
            action_type=action_type,
            detail=detail,
            x=x,
            y=y,
            screenshot_before=None,
            screenshot_after=None
        )

    print(f"[Simulator] Added {num_actions} actions")
