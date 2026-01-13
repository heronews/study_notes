from pydantic import BaseModel


class CustomResponse[T](BaseModel):
    code: int
    msg: str
    data: T | None


class CustomPage[T](BaseModel):
    total: int
    data: list[T]


def make_custom_response[T](code: int, msg: str, data: T | None):
    return CustomResponse[T](code=code, msg=msg, data=data)
