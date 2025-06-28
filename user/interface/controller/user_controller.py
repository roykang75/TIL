from fastapi import APIRouter, Depends
from pydantic import BaseModel
from containers import Container
from user.application.user_service import UserService
from user.domain.user import UserResponse
from dependency_injector.wiring import inject, Provide

router = APIRouter(prefix="/users")


class CreateUserBody(BaseModel):
    name: str
    email: str
    password: str
    memo: str | None


class UpdateUser(BaseModel):
    name: str | None = None
    password: str | None = None


class UsersResponse(BaseModel):
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


@router.get("", response_model=UsersResponse)
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