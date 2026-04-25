from src.simulator import simulate_session
import src.database as db

db.init_db()
simulate_session("workflow_recording_01", num_actions=60)
simulate_session("workflow_recording_02", num_actions=45)
print("\nDone. Now run: python3 main.py")
