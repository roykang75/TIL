from datetime import datetime
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr, Field
from containers import Container
from user.application.user_service import UserService
from dependency_injector.wiring import inject, Provide

router = APIRouter(prefix="/users")


class CreateUserBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(min_length=6, max_length=64)
    password: str = Field(min_length=8, max_length=32)
    memo: str | None = None


class UpdateUser(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime


class GetUsersResponse(BaseModel):
    total_count: int
    page: int
    users: list[UserResponse]


@router.post("", status_code=201, response_model=UserResponse)
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    created_user = user_service.create_user(
        user.name, user.email, user.password, user.memo
    )
    return created_user


@router.put("/{user_id}", response_model=UserResponse)
@inject
def update_user(
    user_id: str,
    user: UpdateUser,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    updated_user = user_service.update_user(user_id, user.name, user.password)
    return updated_user


@router.get("", response_model=GetUsersResponse)
@inject
def get_users(
    page: int = 1,
    items_per_page: int = 10,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    total_count, users = user_service.get_users(page, items_per_page)
    return {
        "total_count": total_count,
        "page": page,
        "users": users,
    }


@router.delete("/{user_id}", status_code=204)
@inject
def delete_user(
    user_id: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    user_service.delete_user(user_id)

@router.post("/login")
@inject
def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    access_token = user_service.login(email=form_data.username, password=form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}

