from sqlalchemy import Table, Column, Integer, String
from ..database import sql_metadata
from pydantic import BaseModel

permission_table = Table(
    "permission",
    sql_metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)


class Permission(BaseModel):
    id: int
    name: str
