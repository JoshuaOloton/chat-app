from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.services.user import UserService
from api.schemas.user import UserResponse
from api.db.database import get_db
from typing import List

user_router = APIRouter(prefix='/users', tags=['User'])


@user_router.get('/', response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return UserService.get_all_users(db)


@user_router.get('/<int:id>', response_model=List[UserResponse])
def get_user(id, db: Session = Depends(get_db)):
    return UserService.get_user_by_id(db, id)