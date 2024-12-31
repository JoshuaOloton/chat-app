from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated

from api.db.database import get_db
from api.db.models import User
from config import settings
from api.schemas.auth import TokenData, RegisterBase
from api.services.token import TokenService
from api.utils.validators import is_valid_email, is_valid_password
from api.utils.hash import PasswordHasher


ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthService:
    """ Service class for authentication. """
     

    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
        """ Get current user from token. """

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        token_data: TokenData = TokenService.verify_access_token(token, credentials_exception)
        
        user = db.query(User).filter(User.id == token_data.id).first()

        if user is None:
            raise credentials_exception
        
        return user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        """ Authenticate user using email and password. """

        if not is_valid_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid email address.'
            )
        
        user = db.query(User).filter(User.email == email).first()

        if not user or not PasswordHasher.verify_password(user.password, password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect credentials.'
            )
    
        return user


    @staticmethod
    def create(db: Session, schema: RegisterBase):
        """ Create user """

        if not is_valid_email(schema.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid email address.'
            )
    

        user = db.query(User).filter(User.email == schema.email).first()

        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'User with email {schema.email} already exists.'
            )
        
        if not is_valid_password(schema.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.'
            )
        
        try:
            user = User(
                email=schema.email,
                fullname=schema.fullname,
                password=PasswordHasher.generate_hash(schema.password)
            )

            db.add(user)
            db.commit()
            db.refresh(user)
            return user

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='An unexpected error occurred while creating user.'
            )
    
