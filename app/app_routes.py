import os

from flask import Blueprint, abort, jsonify, request
from loadotenv import load_env
from sqlalchemy import text

app_bp = Blueprint("auth", __name__)


@app_bp.route("/", methods=["GET"])
def index():
    return {"message": "Bienvenue dans mon application de test 😊"}


@app_bp.route("/health", methods=["GET"])
def health():
    try:
        # requests.get(APP_URL, headers={"X-Health-Token": "supersecret"})
        token = request.headers.get("X-Health-Token")
        if token:
            if token != os.getenv("HEALTH_TOKEN"):
                abort(403)
        # Test DB réel
        session.execute(text("SELECT 1"))
        session.commit()

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
