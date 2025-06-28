from fastapi import HTTPException, Depends
from ulid import ULID
from datetime import datetime
from user.domain.user import User, UserResponse
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository
from utils.crypto import Crypto
from dependency_injector.wiring import inject, Provide

class UserService:
  @inject
  def __init__(
      self, 
      user_repo: IUserRepository = Provide["user_repo"]
  ):
    self.user_repo = user_repo
    self.ulid = ULID()
    self.crypto = Crypto()

  def create_user(self, name: str, email: str, password: str) -> UserResponse:
    _user = None
    
    try:
      _user = self.user_repo.find_by_email(email)
    except HTTPException as e:
      if e.status_code != 422:
        raise e
    
    if _user:
      raise HTTPException(status_code=422)
    
    now = datetime.now()
    user: User = User(
      id=self.ulid.generate(),
      name=name,
      email=email,
      password=self.crypto.encrypt(password),
      created_at=now,
      updated_at=now,
    )
    self.user_repo.save(user)

    return UserResponse(
      id=user.id,
      name=user.name,
      email=user.email,
      created_at=user.created_at,
      updated_at=user.updated_at
    )