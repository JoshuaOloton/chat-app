from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas.user import UserResponse
from api.services.auth import AuthService
from api.services.user import UserService
from api.db.database import get_db
from api.db.models import User
from typing import List

user_router = APIRouter(prefix='/users', tags=['User'])


# @user_router.get('/', response_model=List[UserResponse])
# def get_users(db: Session = Depends(get_db)):
#     return UserService.get_all_users(db)


@user_router.get('/<int:id>', response_model=UserResponse)
def get_user(id, db: Session = Depends(get_db)):
    return UserService.get_user_by_id(db, id)


@user_router.get('/me', response_model=UserResponse)
def get_me(user: UserResponse = Depends(AuthService.get_current_user)):
    return user


@user_router.get('/', response_model=List[UserResponse])
def get_users_for_sidebar(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    return UserService.get_all_users_except_me(db, current_user)
