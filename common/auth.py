from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from enum import StrEnum
from fastapi.security import OAuth2PasswordBearer
from config import get_settings

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

SECRET_KEY = settings.jwt_secret_key
ALGORITHM = "HS256"

class Role(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"


def create_access_token(payload: dict, role: Role, expires_delta: timedelta = timedelta(hours=6)):
    expire = datetime.utcnow() + expires_delta
    payload.update(
        {
          "role": role,
          "exp": expire
        }
    )
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

@dataclass
class CurrentUser:
    id: str
    role: Role

    def __str__(self):
        return f"CurrentUser(id={self.id}, role={self.role})"

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    role = payload.get("role")

    if not user_id or not role or role != Role.USER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return CurrentUser(user_id, role)

def get_admin_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    role = payload.get("role")

    if not user_id or not role or role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return CurrentUser("ADMIN_USEDR_ID", role)