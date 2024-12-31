from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jwt.exceptions import InvalidTokenError
from typing import Annotated, Optional
import jwt

from config import settings
from api.schemas.auth import TokenData


ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenService:
    """ Token handler service """

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """ Create access token. """
        to_encode = data.copy()

        if expires_delta is not None:
            expires = datetime.now() + expires_delta
        else:
            expires = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expires, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
        """ Create refresh token. """

        to_encode = data.copy()

        if expires_delta is not None:
            expires = datetime.now() + expires_delta
        else:
            expires = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expires, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt
    

    @staticmethod
    def verify_access_token(token: Annotated[str, Depends(oauth2_scheme)], credentials_exception: HTTPException) -> TokenData:
        """ Verify access token. """

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

            user_id: str = payload.get("sub")
            type: str = payload.get("type")

            if user_id is None:
                raise credentials_exception
            
            if type != 'access':
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid token type.'
                )
            
            token_data = TokenData(id=user_id)

            return token_data

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token has expired."
            )

        except InvalidTokenError:
            raise credentials_exception  
        
    
    @staticmethod
    def verify_refresh_token(token: str, credentials_exception: HTTPException) -> TokenData:
        """ Verify refresh token. """

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

            user_id: str = payload.get("sub")
            type: str = payload.get("type")

            if user_id is None:
                raise credentials_exception
            
            if type != 'refresh':
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid token type.'
                )
            
            token_data = TokenData(id=user_id)

            return token_data

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired."
            )

        except InvalidTokenError:
            raise credentials_exception 
        


    @staticmethod
    def refresh_access_token(old_refresh_token: str):
        """ Refresh access token using refresh token. """

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is invalid.",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            token: TokenData = TokenService.verify_refresh_token(old_refresh_token, credentials_exception)

            if token:
                access_token = TokenService.create_access_token(data={'type': 'access'})
                refresh_token = TokenService.create_refresh_token(data={'type': 'refresh'})

                return access_token, refresh_token

        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='An unexpected error occurred while refreshing access token.'
            )
    