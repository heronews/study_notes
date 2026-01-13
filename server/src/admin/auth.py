from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated, Any
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.param_functions import Form
import jwt
from .settings import app_settings
from .repositories import user as user_repo, user_session as user_session_repo
from datetime import datetime, timedelta
from passlib.hash import argon2
from .models.auth import JwtPayload
from .models.user import User
from .models.user_session import UserSession, UserSessionInsert
from .models.custom import make_custom_response

security = HTTPBearer()


def hash_password(password: str):
    return argon2.hash(password)


def verify_password(password: str, hash: str):
    return argon2.verify(password, hash)


def encode_jwt(v: dict[str, Any]):
    return jwt.encode(v, app_settings.jwt_key, app_settings.jwt_algorithm)


def decode_jwt(v: str):
    return jwt.decode(v, app_settings.jwt_key, [app_settings.jwt_algorithm])


async def get_current_user_session(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    try:
        payload = JwtPayload.model_validate(decode_jwt(credentials.credentials))
        user_session = user_session_repo.select_by_id(payload.sid)
        if not user_session:
            raise HTTPException(
                status_code=400, detail="can not get current user_session"
            )
        return user_session
    except:
        raise HTTPException(status_code=400, detail="can not get current user_session")


def make_user_has_permission(permission_name: str):
    async def user_has_permission(
        user_session: Annotated[UserSession, Depends(get_current_user_session)],
    ):
        if (
            user_repo.select_count_permission_by_params(
                user_session.user_id, permission_name
            )
            == 1
        ):
            return user_session
        else:
            raise HTTPException(status_code=400, detail="user not has permission")

    return user_has_permission


def init_auth(app: FastAPI):
    @app.post("/login")
    async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
        user = user_repo.select_by_username(username)
        if not user:
            raise HTTPException(status_code=400, detail="user is not exist")
        if not verify_password(password, user.password):
            raise HTTPException(status_code=400, detail="incorrect password")
        user_session = UserSessionInsert(
            user_id=user.id, expire_time=datetime.now() + timedelta(seconds=3600)
        )
        sid = user_session_repo.insert_one(user_session)
        return encode_jwt(
            JwtPayload(sid=sid, exp=user_session.expire_time).model_dump()
        )

    @app.post("/logout")
    async def logout(
        user_session: Annotated[UserSession, Depends(get_current_user_session)],
    ):
        user_session_repo.delete_by_id(user_session.id)
        return make_custom_response(code=1, msg="", data=None)

    @app.post("refresh")
    async def refresh(
        user_session: Annotated[UserSession, Depends(get_current_user_session)],
    ):
        pass
