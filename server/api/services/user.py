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