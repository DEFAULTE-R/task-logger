from flask import Flask, send_from_directory
import src.database as db
from src.simulator import run_simulation

app = Flask(__name__, static_folder="web")

@app.route("/")
def index():
    return send_from_directory("web", "index.html")

# keep your API routes here

if __name__ == "__main__":
    db.init_db()
    run_simulation()  # 👈 THIS LINE
    app.run(host="0.0.0.0", port=5000)
