import json
from pathlib import Path
from datetime import datetime
import src.database as db

def export_dataset(session_id=None, approved_only=True, output_dir="exports"):
    Path(output_dir).mkdir(exist_ok=True)

    actions = db.get_actions(session_id=session_id, limit=10000)

    if approved_only:
        actions = [a for a in actions if a['approved'] == 1]

    dataset = []
    for a in actions:
        dataset.append({
            "id": a['id'],
            "timestamp": a['timestamp'],
            "action_type": a['action_type'],
            "detail": a['detail'],
            "coordinates": {"x": a['x'], "y": a['y']},
            "label": a['label'],
            "screenshot_before": a['screenshot_before'],
            "screenshot_after": a['screenshot_after'],
        })

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/dataset_{ts}.json"

    with open(filename, "w") as f:
        json.dump({
            "exported_at": ts,
            "total_examples": len(dataset),
            "approved_only": approved_only,
            "schema": {
                "action_type": "mouse_click | key_press | scroll | drag | type",
                "detail": "specific action detail",
                "coordinates": "x,y on screen",
                "label": "human-verified label",
                "screenshot_before": "path to screen state before action",
                "screenshot_after": "path to screen state after action"
            },
            "examples": dataset
        }, f, indent=2)

    print(f"[Exporter] Exported {len(dataset)} examples → {filename}")
    return filename, len(dataset)
