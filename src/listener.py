import time
from datetime import datetime
from pynput import keyboard, mouse

events = []

def get_timestamp():
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")

# ---------- KEYBOARD ----------
def on_press(key):
    try:
        events.append({
            "type": "key_press",
            "key": str(key.char),
            "timestamp": get_timestamp()
        })
    except AttributeError:
        events.append({
            "type": "key_press",
            "key": str(key),
            "timestamp": get_timestamp()
        })

# ---------- MOUSE ----------
def on_click(x, y, button, pressed):
    if pressed:
        events.append({
            "type": "mouse_click",
            "button": str(button),
            "position": (x, y),
            "timestamp": get_timestamp()
        })

def on_move(x, y):
    # light sampling (avoid spam)
    if len(events) % 10 == 0:
        events.append({
            "type": "mouse_move",
            "position": (x, y),
            "timestamp": get_timestamp()
        })

# ---------- RUN ----------
def start_listeners():
    print("[Listener] Started...")

    kb_listener = keyboard.Listener(on_press=on_press)
    ms_listener = mouse.Listener(on_click=on_click, on_move=on_move)

    kb_listener.start()
    ms_listener.start()

    return kb_listener, ms_listener

def get_events():
    return events
