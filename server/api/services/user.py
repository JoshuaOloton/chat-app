from api.db.models import User
from typing import List
from sqlalchemy.orm import Session


class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        return db.query(User).get(user_id)
    
    @staticmethod
    def get_all_users(db: Session) -> List[User]:
        return db.query(User).all()
    
    @staticmethod
    def get_all_users_except_me(db: Session, current_user: User) -> List[User]:
        return db.query(User).filter(User.id != current_user.id).all()