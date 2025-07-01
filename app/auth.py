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


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
        
async def get_current_customer(session: SessionDep, token: str = Depends(oauth2_scheme)) -> Customer:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise InvalidTokenException
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise InvalidPasswordException(HTTPStatus.BAD_REQUEST, detail="Invalid Credentials")
    user = await customer_client.fetch_user(username)
    if not user:
        raise UserNotFoundException(HTTPStatus.NOT_FOUND, detail="User Not Found")
    return user

async def get_current_active_customer(
    self, 
    session: Session, 
    token: str
):
    current_customer = self.get_current_customer(session=session, token=token)
    return current_customer
    
def role_required(roles: List[str]):
    async def checker(current_customer: Customer = Depends(get_current_customer)):
        if not current_customer.role.value in roles:
            raise UnauthorizedException(HTTPStatus.UNAUTHORIZED, detail="User unauthorized")
        return current_customer
    return checker
