from dataclasses import dataclass
from pydantic import BaseModel
from datetime import datetime
#from typing import Optional

@dataclass
class Profile(BaseModel):
    name: str
    email: str

@dataclass
class User(BaseModel):
    id: str
    name: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime

@dataclass
class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
    