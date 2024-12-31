from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session
from datetime import timedelta

from api.db.database import get_db
from api.schemas.auth import LoginBase, RegisterBase, LoginResponse, RegisterResponse, RefreshTokenResponse
from api.services.auth import AuthService
from api.services.token import TokenService



auth_router = APIRouter(prefix='/auth', tags=['Auth'])

@auth_router.post('/login', response_model=LoginResponse)
def login(user: LoginBase, response: Response, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, user.email, user.password)
    access_token = TokenService.create_access_token(data={'sub': str(user.id)}) 
    refresh_token = TokenService.create_refresh_token(data={'sub': str(user.id)}) 

    # Add refresh token to cookies
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=timedelta(days=30),
        httponly=True,
        secure=True,
        samesite="none",
    )

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user': {
            "email": user.email,
            "fullname": user.fullname
        }
    }


@auth_router.post('/register', response_model=RegisterResponse)
def register(user: RegisterBase, response: Response, db: Session = Depends(get_db)):
    user = AuthService.create(db, user)

    access_token = TokenService.create_access_token(data={'sub': str(user.id)}) 
    refresh_token = TokenService.create_refresh_token(data={'sub': str(user.id)}) 

    # Add refresh token to cookies
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=timedelta(days=30),
        httponly=True,
        secure=True,
        samesite="none",
    )

    return {
        'message': 'User created successfully',
        'access_token': access_token,
        'token_type': 'bearer',
        'user': {
            'email': user.email,
            'fullname': user.fullname
        }
    }


@auth_router.post('/logout')
def logout(response: Response):
    # Remove refresh token from cookies
    response.delete_cookie('refresh_token')

    return {'message': 'Logout Successful'}


@auth_router.post('/refresh', response_model=RefreshTokenResponse)
def refresh(response: Response, request: Request):
    """ Refresh access token. """

    refresh_token = request.cookies.get('refresh_token')

    access_token, refresh_token = TokenService.refresh_access_token(
        old_refresh_token=refresh_token)

    # Add refresh token to cookies
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=timedelta(days=30),
        httponly=True,
        secure=True,
        samesite="none",
    )

    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }