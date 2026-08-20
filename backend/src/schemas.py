from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Sequence


class TagBase(BaseModel):
    name: str = Field(max_length=50)


class Tag(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class NoteBase(BaseModel):
    header: str = Field(max_length=50)
    text: str | None = None


class NoteOnCreate(NoteBase):
    tags: list[str] = []


class Note(NoteBase):
    id: int
    created_at: datetime
    tags: list[Tag]

    model_config = ConfigDict(from_attributes=True)


class PaginatedNotesResponse(BaseModel):
    items: Sequence[Note]
    total: int
    page: int
    size: int
    pages: int
