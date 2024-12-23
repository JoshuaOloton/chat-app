from pydantic import BaseModel, ConfigDict
from typing import Optional


class TokenData(BaseModel):
    id: Optional[str] = None
    

class LoginBase(BaseModel):
    email: str
    password: str


class UserAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    username: str


class LoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str
    user: UserAuth


class RegisterBase(BaseModel):
    email: str
    username: str
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    username: str
    fullname: str


class RegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message: str
    user: UserAuth