from sanic_jwt import exceptions
from tinydb import Query

from src.db import users_db
from src.definitions import User


async def authenticate(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = users_db.get(Query()["username"] == username)
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    user = User(**user)

    if password != user.password:
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    return user
