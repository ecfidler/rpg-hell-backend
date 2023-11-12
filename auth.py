# Probably a temporary file for testing FastAPI with OAuth2 shidt
from models import User, UserDBModel

fake_users_db = {  # this will be replaced with a table in the database :)
    "ethan": {
        "username": "ethan",
        "email": "ethan@example.com",
        "is_admin": 1,
        "hashed_password": "fakehashedethan",
    },
    "josh": {
        "username": "josh",
        "email": "josh@example.com",
        "is_admin": 1,
        "hashed_password": "fakehashedjosh",
    },
    "ben": {
        "username": "ben",
        "email": "ben@example.com",
        "is_admin": 0,
        "hashed_password": "fakehashedben",
    }
}


def fake_hash_password(password: str):
    return "fakehashed" + password


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserDBModel(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user
