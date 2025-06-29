from dataclasses import asdict
from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from common.auth import CurrentUser, get_current_user
from containers import Container
from note.application.note_service import NoteService
from user.domain.user import User
from dependency_injector.wiring import inject, Provide

router = APIRouter(prefix="/notes")


class NoteResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    memo_date: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime


class CreateNoteBody(BaseModel):
    title: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1)
    memo_date: str = Field(min_length=8, max_length=8)
    tags: list[str] | None = Field(default=None, min_length=1, max_length=32)


@router.post("", status_code=201, response_model=NoteResponse)
@inject
def create_note(
    body: CreateNoteBody,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = note_service.create_note(
        current_user.id,
        body.title,
        body.content,
        body.memo_date,
        body.tags if body.tags else [],
    )

    response = asdict(note)
    response.update({"tags": [tag.name for tag in note.tags]})

    return response


class GetNotesResponse(BaseModel):
    total_count: int
    page: int
    notes: list[NoteResponse]


@router.get("", response_model=GetNotesResponse)
@inject
def get_notes(
    page: int = 1,
    items_per_page: int = 10,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    total_count, notes = note_service.get_notes(current_user.id, page, items_per_page)

    res_notes = []
    for note in notes:
        note_dict = asdict(note)
        note_dict.update({"tags": [tag.name for tag in note.tags]})
        res_notes.append(note_dict)

    return {"total_count": total_count, "page": page, "notes": res_notes}


@router.get("/{id}", response_model=NoteResponse)
@inject
def get_note_by_id(
    id: str,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = note_service.get_note_by_id(current_user.id, id)

    response = asdict(note)
    response.update({"tags": [tag.name for tag in note.tags]})

    return response


class UpdateNoteBody(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=64)
    content: str | None = Field(default=None, min_length=1)
    memo_date: str | None = Field(default=None, min_length=8, max_length=8)
    tags: list[str] | None = Field(default=None)


@router.put("/{id}", response_model=NoteResponse)
@inject
def update_note(
    id: str,
    body: UpdateNoteBody,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = note_service.update_note(
        current_user.id, id, body.title, body.content, body.memo_date, body.tags
    )
    response = asdict(note)
    response.update({"tags": [tag.name for tag in note.tags]})

    return response


@router.delete("/{id}", status_code=204)
@inject
def delete_note(
    id: str,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note_service.delete_note(current_user.id, id)


@router.get("/tags/{tag_name}", response_model=GetNotesResponse)
@inject
def get_notes_by_tag(
    tag_name: str,
    page: int = 1,
    items_per_page: int = 10,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    total_count, notes = note_service.get_notes_by_tag_name(
        current_user.id, tag_name, page, items_per_page
    )

    res_notes = []
    for note in notes:
        note_dict = asdict(note)
        note_dict.update({"tags": [tag.name for tag in note.tags]})
        res_notes.append(note_dict)

    return {"total_count": total_count, "page": page, "notes": res_notes}
