from pydantic import BaseModel
from datetime import datetime
#from typing import Optional

class Profile(BaseModel):
    name: str
    email: str

class User(BaseModel):
    id: str
    name: str
    email: str
    password: str
    memo: str | None
    created_at: datetime
    updated_at: datetime

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    memo: str | None
    created_at: datetime
    updated_at: datetime
    