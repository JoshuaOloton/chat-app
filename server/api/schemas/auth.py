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
    fullname: str


class LoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str
    user: UserAuth


class RegisterBase(BaseModel):
    email: str
    fullname: str
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    fullname: str


class RegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message: str
    access_token: str
    token_type: str
    user: UserAuth


class RefreshTokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str
