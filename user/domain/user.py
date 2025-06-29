from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: str
    name: str
    email: str
    password: str
    memo: str | None
    created_at: datetime
    updated_at: datetime