from sqlalchemy import Table, Column, Integer, String
from ..database import sql_metadata
from pydantic import BaseModel
from datetime import datetime

user_session_table = Table(
    "user_session",
    sql_metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("expire_time", String),
)


class UserSession(BaseModel):
    id: int
    user_id: int
    expire_time: datetime


class UserSessionInsert(BaseModel):
    user_id: int
    expire_time: datetime
