import os

from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from loadotenv import load_env
from sqlalchemy import text

app = Flask(__name__)

load_env()
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{USER}:{PASSWORD}@localhost:3307/db_test"

db = SQLAlchemy(app)

HEALTH_TOKEN = "supersecret"


@app.route("/", methods=["GET"])
def index():
    return {"message": "Bienvenue dans mon application de test 😊"}


@app.route("/health", methods=["GET"])
def health():
    try:
        # requests.get(APP_URL, headers={"X-Health-Token": "supersecret"})
        if token:
            token = request.headers.get("X-Health-Token")
            if token != HEALTH_TOKEN:
                abort(403)
        # Test DB réel
        db.session.execute(text("SELECT 1"))
        db.session.commit()

        return jsonify({"status": "healthy"}), 200

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "unhealthy",
                    "error": "erreur sur la base de données",
                    "message": f"erreur:{e}",
                }
            ),
            500,
        )


if __name__ == "__main__":
    app.run()
