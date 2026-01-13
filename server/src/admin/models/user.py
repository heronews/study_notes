from sqlalchemy import Table, Column, Integer, String, Boolean
from ..database import sql_metadata
from pydantic import BaseModel

user_table = Table(
    "user",
    sql_metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("password", String),
    Column("enable", Boolean),
)


class User(BaseModel):
    id: int
    username: str
    password: str
    enable: bool


class UserInert(BaseModel):
    username: str
    password: str
    enable: bool = True


class UserUpdate(BaseModel):
    id: int
    username: str | None = None
    password: str | None = None
    enable: bool | None = None
