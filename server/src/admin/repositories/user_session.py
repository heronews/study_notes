from sqlalchemy import select, insert, delete
from ..database import sql_engine
from ..models.user_session import user_session_table, UserSession, UserSessionInsert


def select_by_id(id: int):
    with sql_engine.connect() as conn:
        row = conn.execute(
            select(user_session_table).where(user_session_table.c.id == id)
        ).one_or_none()
        if not row:
            return None
        return UserSession(**row._asdict())


def insert_one(user_session: UserSessionInsert):
    with sql_engine.connect() as conn:
        result = conn.execute(
            insert(user_session_table).values(user_session.model_dump())
        )
        conn.commit()
        return result.inserted_primary_key[0]


def delete_by_id(id: int):
    with sql_engine.connect() as conn:
        conn.execute(delete(user_session_table).where(user_session_table.c.id == id))
        conn.commit()
