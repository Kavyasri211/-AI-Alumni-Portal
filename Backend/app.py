from pathlib import Path
import sys
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

from Backend.database import init_db, seed_db
from Backend.routes.auth import bp as auth_bp
from Backend.routes.alumni import bp as alumni_bp
from Backend.routes.events import bp as events_bp
from Backend.routes.messages import bp as messages_bp
from Backend.routes.ai import bp as ai_bp

app = Flask(__name__, static_folder=str(BASE / "Frontend"))
CORS(app)
init_db()
seed_db()

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(alumni_bp, url_prefix="/api/alumni")
app.register_blueprint(events_bp, url_prefix="/api/events")
app.register_blueprint(messages_bp, url_prefix="/api/messages")
app.register_blueprint(ai_bp, url_prefix="/api/ai")

@app.get("/api/health")
def health():
    return jsonify(status="ok")

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def frontend(path):
    p = BASE / "Frontend" / path
    if p.exists() and p.is_file():
        return send_from_directory(BASE / "Frontend", path)
    return send_from_directory(BASE / "Frontend", "index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
