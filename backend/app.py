import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from extensions import db
from dotenv import load_dotenv  # ✅ To load .env file

# ✅ Load environment variables
load_dotenv()

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # ✅ Ensure db directory exists
    os.makedirs("db", exist_ok=True)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, "db", "database.db")

    # ✅ Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ Allow CORS
    CORS(
        app,
        resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}},
        supports_credentials=True,
        allow_headers="*",
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )

    # ✅ Import Blueprints (after db and extensions)
    from routes.activities import activities_bp
    from routes.emissions import emissions_bp
    from routes.achievements import achievements_bp
    from routes.ai import ai_bp
    from routes.log_activity import log_activity_bp
    from routes.community import community_bp
    from routes.stats import stats_bp
    from routes.clear_data import clear_data_bp  # ✅ NEW IMPORT

    # ✅ Register Blueprints
    app.register_blueprint(activities_bp, url_prefix="/api/activities")
    app.register_blueprint(emissions_bp, url_prefix="/api/emissions")
    app.register_blueprint(achievements_bp, url_prefix="/api/achievements")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    app.register_blueprint(log_activity_bp, url_prefix="/api/")
    app.register_blueprint(community_bp, url_prefix="/api")
    app.register_blueprint(stats_bp)
    app.register_blueprint(clear_data_bp)  # ✅ NEW REGISTRATION

    @app.route("/")
    def home():
        return "🌿 GreenPath backend is running with AI support!"

    return app


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()

    app.run(debug=True, host="0.0.0.0", port=5000)
