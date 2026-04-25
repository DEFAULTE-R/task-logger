from flask import Flask, send_from_directory
import src.database as db

app = Flask(__name__, static_folder="web")

@app.route("/")
def index():
    return send_from_directory("web", "index.html")

# (keep your API routes as-is)

if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=5000)
