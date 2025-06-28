from fastapi import APIRouter
from pydantic import BaseModel
from user.application.user_service import UserService

router = APIRouter(prefix="/users")
#@router.post("", status_code=201)
#def create_user(user_service: UserService, name: str, email: str, password: str):
#  return user_service.create_user(name, email, password)

class CreateUserBody(BaseModel):
  name: str
  email: str
  password: str

@router.post("", status_code=201)
def create_user(user: CreateUserBody):
  user_service = UserService()
  created_user = user_service.create_user(user.name, user.email, user.password)
  return created_user