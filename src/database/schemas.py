from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class TagBase(BaseModel):
    name: str


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
    tags: list[Tag] = []

    model_config = ConfigDict(from_attributes=True)
