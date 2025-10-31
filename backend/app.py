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
    os.makedirs("db", exist_ok=True)

    app.url_map.strict_slashes = False

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, "db", "database.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret")


    db.init_app(app)
    migrate.init_app(app, db)

    CORS(
        app,
        resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "https://green-path-pearl.vercel.app"
            ]
        }
    },
        resources = {
    r"/api/*": {
        "origins": [
            "https://green-path-m5yh.vercel.app",  
            "http://localhost:5173",              
            "http://127.0.0.1:5173"
        ]
    }
},

        supports_credentials=True,
    )

    from routes.community import community_bp
    from routes.emissions import emissions_bp
    from routes.ai import ai_bp
    from routes.activities import activities_bp
    from routes.stats import stats_bp
    from routes.achievements import achievements_bp
    from routes.predictions import predictions_bp  

    app.register_blueprint(community_bp)
    app.register_blueprint(emissions_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(activities_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(achievements_bp)
    app.register_blueprint(predictions_bp)

    
    @app.route("/")
    def home():
        return "GreenPath backend is running!"

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  

    import os
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)
        db.create_all() 
    app.run(debug=True, host="127.0.0.1", port=5000)
