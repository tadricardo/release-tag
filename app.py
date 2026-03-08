from flask import jsonify, Flask
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from loadotenv import load_env
import os

app = Flask(__name__)

load_env()
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{USER}:{PASSWORD}@localhost:3307/db_test"

db = SQLAlchemy(app)


@app.route("/", methods=["GET"])
def index():
    return {"message": "Bienvenue dans mon application de test 😊"}


@app.route("/health", methods=["GET"])
def health():
    try:
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
