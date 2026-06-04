from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import schemas
from src.database.schemas import Note as Pydantic_Note
from src.database.models import Note as DB_Note
from src.database.database import get_db

notes_db: dict[int, schemas.Note] = {}

router = APIRouter()

@router.get("/")
async def index():
    return {"ping": "pong"}

@router.get("/notes")
async def get_notes(tag: str | None = None):
    if not tag:
        return list(notes_db.values())
    
    filtered_notes = [note for note in notes_db.values() if tag in note.tags]
    
    return filtered_notes

@router.get("/notes/{note_id}")
async def view_note(note_id: int):
    note = notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note

@router.post("/notes")
async def add_note(note_data: schemas.NoteBase):
    new_id = len(notes_db) + 1
    temp_note: schemas.Note = schemas.Note(
        id=new_id,
        header=note_data.header,
        text=note_data.text,
        tags=note_data.tags,
        created_at=datetime.now()
    )
    notes_db[new_id] = temp_note

    return temp_note

@router.put("/notes/{note_id}")
async def edit_note(note_id: int, note_data: schemas.NoteBase):
    note = notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note.header=note_data.header
    note.text=note_data.text
    note.tags=note_data.tags

    return note

@router.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    note = notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    del notes_db[note_id]
    return {"message": "Note deleted"}

