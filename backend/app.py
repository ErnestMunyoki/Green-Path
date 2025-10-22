from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate  # ✅ NEW import

app = Flask(__name__)

# Allow React frontend access
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/community.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # ✅ Initialize Flask-Migrate

from routes import *  # Import routes after db + migrate setup

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
