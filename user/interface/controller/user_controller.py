from fastapi import APIRouter, Depends
from pydantic import BaseModel
from user.application.user_service import UserService
from user.domain.user import UserResponse
from dependency_injector.wiring import inject, Provide

router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel):
  name: str
  email: str
  password: str

@router.post("", status_code=201, response_model=UserResponse)
@inject
def create_user(
  user: CreateUserBody, 
  user_service: UserService = Depends(Provide["user_service"])
):
  created_user = user_service.create_user(user.name, user.email, user.password)
  return created_user