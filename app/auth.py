from fastapi import Depends
from app.schemas.customer import (
    TokenData, 
    Customer
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from app.exceptions import (
    InvalidPasswordException, 
    InvalidTokenException, 
    UserNotFoundException, 
    UnauthorizedException,
)
from app.deps import SessionDep
from http import HTTPStatus
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timezone, timedelta
from app.core.settings import Settings
from typing import List
from app.clients.customer_client import CustomerClient


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = Settings()
customer_client = CustomerClient()

        
async def get_current_customer_role(session: SessionDep, token: str = Depends(oauth2_scheme)) -> Customer:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        customer_id = payload.get("sub")
        role = payload.get("role")
        if customer_id is None:
            raise InvalidTokenException
        if role is None: 
            raise InvalidTokenException
    except InvalidTokenError:
        raise InvalidPasswordException(HTTPStatus.BAD_REQUEST, detail="Invalid Credentials")
    return role

def role_required(roles: List[str]):
    async def checker(role: str = Depends(get_current_customer_role)):
        print(role)
        if not role in roles:
            raise UnauthorizedException(HTTPStatus.UNAUTHORIZED, detail="User unauthorized")
        return 
    return checker
