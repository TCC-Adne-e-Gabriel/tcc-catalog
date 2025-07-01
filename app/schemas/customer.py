from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Customer(BaseModel): 
    name: str
    email: str
    phone: str
    id: UUID
    created_at: datetime
    updated_at: datetime

class Token(BaseModel): 
    access_token: str
    token_type: str

class TokenData(BaseModel): 
    username: UUID | None = None