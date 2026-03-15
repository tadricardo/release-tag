from datetime import timedelta

from flask_jwt_extended import create_access_token


def generate_token(user_id):
    access_token = create_access_token(
        identity=user_id, expires_delta=timedelta(minutes=5)
    )

    return access_token
