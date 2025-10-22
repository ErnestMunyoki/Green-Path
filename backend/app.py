import os
from flask import Flask
from flask_cors import CORS
from extensions import db, migrate  
def create_app():
    app = Flask(__name__)

    # Ensure db folder exists
    os.makedirs("db", exist_ok=True)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, "db", "database.db")

    # Database config
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import blueprints AFTER init
    from routes.activities import activities_bp
    from routes.emissions import emissions_bp
    from routes.achievements import achievements_bp
    from routes.ai import ai_bp
    from routes.log_activity import log_activity_bp
    from routes.community import community_bp

    # Register blueprints
    app.register_blueprint(activities_bp)
    app.register_blueprint(emissions_bp)
    app.register_blueprint(achievements_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(log_activity_bp)
    app.register_blueprint(community_bp)

    # Enable CORS
    CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"], supports_credentials=True)

    @app.route("/")
    def home():
        return "🌿 GreenPath backend is running!"

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
