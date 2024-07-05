from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exeptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
    UserNotGetException,
    UserRoleException,
)
from app.users.dao import UsersDAO
from app.users.enums import UserRole
from app.users.models import Users


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    try:
        user_id: int = int(user_id)
    except ValueError:
        raise UserNotGetException

    if not user_id:
        raise UserIsNotPresentException

    user = await UsersDAO.find_by_id(model_id=user_id)
    if not user:
        raise UserIsNotPresentException

    return user


async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise UserRoleException
    return current_user
