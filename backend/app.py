import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from extensions import db
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Ensure local db folder exists
    os.makedirs("db", exist_ok=True)

    app.url_map.strict_slashes = False

    # Database configuration
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Use cloud DATABASE_URL if available, else fallback to local sqlite
    DB_URL = os.environ.get("DATABASE_URL")
    if DB_URL:
        app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
    else:
        DB_PATH = os.path.join(BASE_DIR, "db", "database.db")
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_secret")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # -----------------------------
    # Register Blueprints
    # -----------------------------
    from routes.community import community_bp
    from routes.emissions import emissions_bp
    from routes.ai import ai_bp
    from routes.activities import activities_bp
    from routes.stats import stats_bp
    from routes.achievements import achievements_bp
    from routes.predictions import predictions_bp  

    app.register_blueprint(community_bp, url_prefix="/api/community")
    app.register_blueprint(emissions_bp, url_prefix="/api/emissions")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    app.register_blueprint(activities_bp, url_prefix="/api/activities")
    app.register_blueprint(stats_bp, url_prefix="/api/stats")
    app.register_blueprint(achievements_bp, url_prefix="/api/achievements")
    app.register_blueprint(predictions_bp, url_prefix="/api/predictions")

    # -----------------------------
    # Preflight-s
