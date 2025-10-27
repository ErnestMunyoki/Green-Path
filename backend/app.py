import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from extensions import db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

migrate = Migrate()

logging.basicConfig(level=logging.INFO)

def create_app():
    app = Flask(__name__)
    os.makedirs("db", exist_ok=True)

    # ✅ Disable trailing slash redirect globally (must be set early)
    app.url_map.strict_slashes = False

    # ✅ Define database path
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, "db", "database.db")

    # ✅ Database config
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret")

    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ Global CORS config
    CORS(
        app,
        resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # ✅ Import blueprints
    from routes.activities import activities_bp
    from routes.emissions import emissions_bp
    from routes.achievements import achievements_bp
    from routes.ai import ai_bp
    from routes.log_activity import log_activity_bp
    from routes.community import community_bp
    from routes.stats import stats_bp
    from routes.clear_data import clear_data_bp

    # ✅ Register blueprints
    app.register_blueprint(activities_bp, url_prefix="/api/activities")
    app.register_blueprint(emissions_bp, url_prefix="/api/emissions")
    app.register_blueprint(achievements_bp, url_prefix="/api/achievements")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    app.register_blueprint(log_activity_bp, url_prefix="/api")
    app.register_blueprint(community_bp, url_prefix="/api")
    app.register_blueprint(stats_bp, url_prefix="/api")
    app.register_blueprint(clear_data_bp, url_prefix="/api")

    @app.route("/")
    def home():
        return jsonify({"message": "🌿 GreenPath backend is running with AI support!"})

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()

    app.run(debug=True, host="127.0.0.1", port=5000)
