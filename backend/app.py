import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from extensions import db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    os.makedirs("db", exist_ok=True)

    # Disable trailing slash redirects
    app.url_map.strict_slashes = False

    # Database configuration
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, "db", "database.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Enable global CORS for frontend
    CORS(
        app,
        resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}},
        supports_credentials=True,
    )

    # Import and register blueprints
    from routes.community import community_bp
    from routes.emissions import emissions_bp
    from routes.ai import ai_bp
    from routes.activities import activities_bp
    from routes.stats import stats_bp
    from routes.achievements import achievements_bp
    from routes.predictions import predictions_bp  # <- import predictions

    app.register_blueprint(community_bp)
    app.register_blueprint(emissions_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(activities_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(achievements_bp)
    app.register_blueprint(predictions_bp)  # <- register predictions

    # Basic home route
    @app.route("/")
    def home():
        return "🌿 GreenPath backend is running!"

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # Ensure database tables exist
    app.run(debug=True, host="127.0.0.1", port=5000)

app = create_app()