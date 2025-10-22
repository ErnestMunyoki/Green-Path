import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from routes.activities import activities_bp
from routes.emissions import emissions_bp
from routes.achievements import achievements_bp
from routes.ai import ai_bp
from routes.log_activity import log_activity_bp

# Ensure db folder exists
os.makedirs("db", exist_ok=True)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "database.db")

app = Flask(__name__)

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Allow frontend (React) access
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Register routes
app.register_blueprint(activities_bp)
app.register_blueprint(emissions_bp)
app.register_blueprint(achievements_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(log_activity_bp)

@app.route("/")
def home():
    return "GreenPath backend is running!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
