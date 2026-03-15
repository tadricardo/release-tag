from .jwt_handler import generate_token
from .password_handler import verify_password

# exemple simple
users = {"admin": {"password": "$2b$12$xxxxxxxxxxxxxxxxxxxxxxxx"}}


def login_user(username, password):
    user = users.get(username)

    if not user:
        return None

    if not verify_password(password, user["password"]):
        return None

    token = generate_token(username)

    return token
