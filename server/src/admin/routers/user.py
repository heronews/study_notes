from fastapi import APIRouter, Depends
from typing import Annotated
from ..repositories import user as user_repo
from ..models.user import User, UserInert
from ..models.user_session import UserSession
from ..models.custom import make_custom_response
from ..auth import hash_password, make_user_has_permission


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users(
    user_session: Annotated[
        UserSession, Depends(make_user_has_permission("user:select"))
    ],
    page: int,
    size: int,
):
    return make_custom_response(code=1, msg="", data=user_repo.select_page(page, size))


@router.post("/register")
async def register(user: UserInert):
    user.password = hash_password(user.password)
    user_repo.insert_one(user)
    return make_custom_response(code=1, msg="", data=None)
