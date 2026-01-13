from sqlalchemy import Table, Column, Integer, String
from ..database import sql_metadata
from pydantic import BaseModel

role_table = Table(
    "role",
    sql_metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)


class Role(BaseModel):
    id: int
    name: str
