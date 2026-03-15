from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from .app_routes import app_bp
from .auth_routes import auth_bp
from .config import Config

jwt = JWTManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)
    bcrypt.init_app(app)

    CORS(app)
    SQLAlchemy(app=app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(app_bp)

    return app
