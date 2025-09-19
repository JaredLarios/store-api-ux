from pydantic import BaseModel


class Token(BaseModel):
    sub: str
    iss: str
    iat: int | float
    exp: int | float


class AccessToken(Token):
    name: str
    role: str
