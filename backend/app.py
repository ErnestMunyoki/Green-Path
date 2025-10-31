import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from extensions import db
from dotenv import load_dotenv

load_dotenv()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_URL = os.environ.get("DATABASE_URL")
    if DB_URL:
        app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
    else:
        DB_PATH = os.environ.get("SQLITE_PATH", os.path.join("/tmp", "database.db"))
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_secret")
    app.url_map.strict_slashes = False

    db.init_app(app)
    migrate.init_app(app, db)

   
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

    
    cors_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://green-path-pearl.vercel.app",
        "https://green-path-m5yh.vercel.app"
    ]

    CORS(
        app,
        resources={r"/api/*": {"origins": cors_origins}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

   
    @app.route("/")
    def home():
        return "GreenPath backend is running!"

    
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
