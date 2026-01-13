from pydantic import BaseModel
from datetime import datetime


class JwtPayload(BaseModel):
    sid: int
    exp: datetime


# class Oauth2Model(BaseModel):
#     access_token: str
#     token_type: str
#     refresh_token: str
#     expires_in: int
#     scope: str
