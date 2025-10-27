import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from extensions import db
from dotenv import load_dotenv
from datetime import datetime  # merged addition

load_dotenv()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    os.makedirs("db", exist_ok=True)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, "db", "database.db")

    # ✅ Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ Enable CORS for frontend
    CORS(
        app,
        resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}},
        supports_credentials=True,
    )

    # ✅ Import and register routes
    from routes.activities import activities_bp
    from routes.emissions import emissions_bp
    from routes.achievements import achievements_bp
    from routes.ai import ai_bp
    from routes.log_activity import log_activity_bp
    from routes.community import community_bp
    from routes.stats import stats_bp
    from routes.clear_data import clear_data_bp
    from routes.predictions import prediction_bp  

    # ✅ Register all Blueprints (no duplicate prefixes)
    app.register_blueprint(activities_bp, url_prefix="/api/activities")
    app.register_blueprint(emissions_bp, url_prefix="/api/emissions")
    app.register_blueprint(achievements_bp, url_prefix="/api/achievements")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    app.register_blueprint(log_activity_bp, url_prefix="/api")
    app.register_blueprint(community_bp, url_prefix="/api/community")
    app.register_blueprint(stats_bp, url_prefix="/api/stats")
    app.register_blueprint(clear_data_bp, url_prefix="/api/clear")
    app.register_blueprint(prediction_bp, url_prefix="/api/predictions")

    @app.route("/")
    def home():
        return "🌿 GreenPath backend is running with AI, stats, and emissions tracking!"

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
