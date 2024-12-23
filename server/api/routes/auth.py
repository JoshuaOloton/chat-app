from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.db.database import get_db
from api.schemas.auth import LoginBase, RegisterBase, LoginResponse, RegisterResponse



auth_router = APIRouter(prefix='/auth', tags=['Auth'])

@auth_router.post('/login', response_model=LoginResponse)
def login(user: LoginBase, db: Session = Depends(get_db)):
    return {'message': 'Login'}


@auth_router.post('/register')
def register():
    return {'message': 'Register'}


@auth_router.post('/logout')
def logout():
    return {'message': 'Logout Successful'}