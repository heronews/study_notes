from sqlalchemy import select, func, insert, update, text
from ..database import sql_engine
from ..models.user import user_table, User, UserInert, UserUpdate
from ..models.custom import CustomPage


def select_page(page: int, size: int):
    with sql_engine.connect() as conn:
        return CustomPage[User](
            total=conn.execute(
                select(func.count().label("total")).select_from(user_table)
            )
            .one()
            .total,
            data=[
                i._asdict()
                for i in conn.execute(
                    select(user_table).offset((page - 1) * size).limit(size)
                )
            ],
        )


def select_by_username(username: str):
    with sql_engine.connect() as conn:
        row = conn.execute(
            select(user_table).where(user_table.c.username == username)
        ).one_or_none()
        if not row:
            return None
        return User(**row._asdict())


def insert_one(user: UserInert):
    with sql_engine.connect() as conn:
        conn.execute(insert(user_table).values(user.model_dump()))
        conn.commit()


def update_one(user: UserUpdate):
    with sql_engine.connect() as conn:
        conn.execute(
            update(user_table)
            .where(user_table.c.id == user.id)
            .values(user.model_dump(exclude_unset=True, exclude={"id"}))
        )
        conn.commit()


def select_count_permission_by_params(user_id: int, permission_name: str):
    with sql_engine.connect() as conn:
        return (
            conn.execute(
                text(
                    "SELECT count(*) AS total "
                    "FROM user_role AS a "
                    "INNER JOIN role_permission AS b ON a.role_id = b.role_id "
                    "INNER JOIN permission AS c ON b.permission_id = c.id "
                    "WHERE a.user_id = :user_id AND c.name = :permission_name"
                ),
                {"user_id": user_id, "permission_name": permission_name},
            )
            .one()
            .total
        )
