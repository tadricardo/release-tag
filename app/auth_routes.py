from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from .auth_service import login_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    token = login_user(username, password)

    if not token:
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"access_token": token})


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify({"message": "Access granted"})
